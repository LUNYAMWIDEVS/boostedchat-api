from rest_framework import serializers, viewsets, routers
from django.apps import apps
import sys
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from base.helpers.push_id import PushID
from rest_framework import generics, mixins, views
from django.http import QueryDict
import json
from setup.utils import modelManager


class APIRouterGenerator:
    """
    Generates serializers and viewsets for Django models with the `autoLoad` attribute.
    """

    def __init__(self):
        self.module = sys.modules[__name__]
        self.auto_apps_models = [
            model for model in apps.get_models() if hasattr(model, 'autoLoad') and model.autoLoad
        ]
        self.api_serializers = self.make_api_serializers(self.auto_apps_models)
        self.api_viewsets = self.make_api_viewsets(self.auto_apps_models, self.api_serializers)
        self.rest_api_urls = self.create_rest_api_urls()
        self.router = self.create_router()

    @staticmethod
    def listMethods():
        return ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
    
    def has_fields(self, model_class, *fields):
        """Check if the model class has all the specified fields."""
        return all(hasattr(model_class, field) for field in fields)

    def make_api_serializers(self, api_models, base_serializer_class=serializers.ModelSerializer):
        api_serializers = []
        for ModelClass in api_models:
            class_name = f'{ModelClass.__name__}Serializer'
            exclude_fields_for_methods = {
                "POST": ('id',),
                "GET": (),
                "PUT": (),
                # "PATCH": ('created_at', 'updated_at', 'deleted_at'),
                "PATCH": (),
                "DELETE": (),
            }

            if self.has_fields(ModelClass, 'created_at', 'updated_at', 'deleted_at'):
                exclude_fields_for_methods["PATCH"] = ('created_at', 'updated_at', 'deleted_at')
    
            methods = self.listMethods()
            methods_serializers = {}
            for method in methods:
                def get_model_serializer(ModelClass, method):
                    class_name = f'{ModelClass.__name__}Serializer'

                    class ModelSerializer(base_serializer_class):
                        class Meta:
                            model = ModelClass
                            depth = 10
                            if exclude_fields_for_methods[method]:
                                exclude = exclude_fields_for_methods[method]
                            else:
                                fields = '__all__'
                        # def to_representation(self, instance):
                        #     representation = super().to_representation(instance)
                        #     if self.context['request'].method == 'GET':
                        #         filters = {field.name: field.get_internal_type() for field in self.Meta.model._meta.get_fields()}
                        #         representation['filters'] = filters
                        #     return representation

                        # def validate_id(self, value): # Not working
                        #     if self.context['request'].method == 'POST' and value is not None:
                        #         raise serializers.ValidationError("Cannot specify 'id' when creating a new object.")
                        #     return value

                    ModelSerializer.__name__ = class_name
                    return ModelSerializer

                methods_serializers[method] = get_model_serializer(ModelClass, method)
            api_serializers.append({f"{ModelClass._meta.app_label}.{ModelClass.__name__}": methods_serializers})
        return api_serializers

    def make_api_viewsets(self, api_models, api_serializers):
        api_viewsets = []
        for ModelClass, SerializerClass in zip(api_models, api_serializers):
            table_name = ModelClass._meta.db_table
            app_name = ModelClass._meta.app_label

            def create_viewset(ModelClass, table_name, SerializerClass):
                class ModelViewSet(viewsets.ModelViewSet):
                    db_table = table_name
                    queryset = ModelClass.objects.all()
                    app_name = ModelClass._meta.app_label
                    read_with_data = False

                    def getModelManager(self):
                        if hasattr(ModelClass, 'modelManager'):
                            ret = ModelClass.modelManager
                        else:
                            ret = modelManager
                        return ret

                    def get_permissions(self): # make generic. should have IsAuthenticated classed by default
                        """
                        Instantiates and returns the list of permissions that this view requires.
                        """
                        if hasattr(ModelClass, 'permissionClasses'):
                            permission_classes = ModelClass.permissionClasses
                        elif self.action == 'list':
                            permission_classes = [IsAuthenticated]
                        else:
                            permission_classes = [IsAdminUser]
                        return [permission() for permission in permission_classes]
                    
                    def get_filters_serializer(self,ModelClass):
                        class FiltersSerializer(serializers.Serializer):
                            filters = serializers.JSONField(required=False)

                            def validate_filters(self, value):
                                # Optionally validate filter fields against model fields
                                model_fields = {field.name for field in ModelClass._meta.get_fields()}
                                invalid_fields = [field for field in value.keys() if field not in model_fields]
                                if invalid_fields:
                                    raise serializers.ValidationError(f"Invalid fields: {', '.join(invalid_fields)}")
                                return value

                        return FiltersSerializer

                    def list(self, request): # todo: add filters
                        FiltersSerializer = self.get_filters_serializer(self.get_queryset().model)
                        filters_serializer = FiltersSerializer(data=request.query_params)
                        filters_serializer.is_valid(raise_exception=True)
                        # Serialize the filters data
                        filters_data = filters_serializer.data
                        print("Filters Data", filters_data, filters_serializer.validated_data)
                        ret = self.getModelManager()(ModelClass).read_model(filters_serializer.validated_data)
                        replySerializer = self.get_serializer_class("GET")
                        replySerializer = replySerializer(ret, many=True) # return with id field
                        ret = replySerializer.data   
                        return Response(ret, status=status.HTTP_200_OK) 
                        # return super().list(request)
                    def get(self, request): # quickfix for retrieve. done
                        return super().retrieve(request)
                    def create(self, request): # done
                        modelHasModelManager = hasattr(ModelClass, 'modelManager')
                        if not modelHasModelManager: # set id to avoid serializer error. We have used serializer with id field so that 'id' is also returned after creating record
                            id = PushID().next_id()
                            data = request.data.copy()
                            data['id'] = id
                            request._full_data = data  # This is a hack to get around the fact that the request.data is immutable
                            ret = super().create(request)                        
                            return ret
                        else: # with a model manager supplied
                            # modelHasSerializer = False
                            # serializer = None
                            requestSerializer = None 
                            replySerializer = None
                            # if not modelHasSerializer:
                            #     id = PushID().next_id()
                            #     data = request.data.copy()
                            #     data['id'] = id
                            #     request._full_data = data
                            # else:
                            #     pass
                            id = PushID().next_id()
                            data = request.data.copy()
                            data['id'] = id
                            request._full_data = data
                            
                            requestSerializer = self.get_serializer(data=request.data) # will be either from here or from ModelClass
                            replySerializer = self.get_serializer_class("GET")
                                                        
                            requestSerializer.is_valid(raise_exception=True)
                            ret  = self.getModelManager()(ModelClass).save_model(requestSerializer.validated_data)
                            replySerializer = replySerializer(ret, many=False) # return with id field
                            ret = replySerializer.data                            
                            headers = self.get_success_headers(ret)
                            return Response(ret, status=status.HTTP_201_CREATED,  headers=headers)
                    def destroy(self, request, *args, **kwargs): # done: delete single record (with lookup)
                        return super().destroy(request, *args, **kwargs)
                    def delete(self, request): # delete without lookup
                        raise MethodNotAllowed(method='DELETE', detail='Method "DELETE" not allowed without lookup')
                    def update(self, request, *args, **kwargs): 
                        # return super().update(request, *args, **kwargs)
                        partial = kwargs.pop('partial', False)
                        instance = self.get_object()
                        serializer = self.get_serializer(instance, data=request.data, partial=partial)
                        serializer.is_valid(raise_exception=True)
                        return self.perform_update(serializer)
                    def perform_update(self, serializer):
                        ret = self.getModelManager()(ModelClass).update_model(serializer.validated_data)
                        # ret = serializer.validated_data
                        replySerializer = self.get_serializer_class("GET")
                        replySerializer = replySerializer(ret, many=False) # return with id field
                        ret = replySerializer.data    
                        return Response(ret, status=status.HTTP_201_CREATED)
                    def get_serializer_for_method(self, method):
                        method = method.upper()
                        if not hasattr(ModelClass, 'localSerializers'):
                            return None
                        for serializer_name, serializer_info in ModelClass.localSerializers.items():
                            if method in serializer_info["methods"]:
                                return serializer_info["serializer"]
                        # # If method-specific serializer does not exist, return the default serializer
                        # return self.get_serializer_for_method("default")
                        return None # use the serializer defined here
                    def get_serializer_class(self, method=None):
                        if method is None:
                            method = self.request.method                        
                        serializer = self.get_serializer_for_method(method)
                        if serializer is not None:
                            return serializer
                        if method == "POST":
                            if  self.request.data == {}: # from a different method for displaying in form
                                serializer = SerializerClass[f'{self.app_name}.{ModelClass.__name__}'].get("POST") # for showing in the form. No id
                            else :
                                if self.request.data.get("___read_with_id") == 1:
                                    serializer = SerializerClass[f'{self.app_name}.{ModelClass.__name__}'].get("POST")  # for showing in the form. No id
                                else:

                                    number = self.request.data.get("___read_with_id") if hasattr(self.request.data, "___read_with_id") else 0
                                    number += 1
                                    data = self.request.data.copy()
                                    data['___read_with_id'] = number
                                    self.request._full_data = data
                                    serializer = SerializerClass[f'{self.app_name}.{ModelClass.__name__}'].get("GET") # return data with id field
                        else:
                            serializer = SerializerClass[f'{self.app_name}.{ModelClass.__name__}'].get(method)

                        if serializer is None:
                            raise ValueError(f"No serializer defined for method {method}")
                        return serializer

                return ModelViewSet

            viewset = create_viewset(ModelClass, table_name, SerializerClass)
            api_viewsets.append({f"{app_name}.{ModelClass.__name__}": viewset})
        return api_viewsets

    def create_rest_api_urls(self):
        rest_api_urls = []
        for viewset in self.api_viewsets:
            app_name = list(viewset.keys())[0].lower().split('.')
            k = list(viewset.keys())[0]
            rest_api_urls.append((fr'{app_name[0]}/{app_name[1]}', viewset[k], f'{app_name[0]}/{app_name[1]}'))
        return rest_api_urls

    def create_router(self):
        router = routers.DefaultRouter()
        for route in self.rest_api_urls:
            router.register(route[0], route[1], basename=route[2])
        return router
