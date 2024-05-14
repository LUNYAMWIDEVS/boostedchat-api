from rest_framework import serializers, viewsets, routers
from django import apps
import sys

module = sys.modules[__name__]
# "module/sys.modules" is a list of all the system files that are loading into memory at run time.
# There are for loops below that bolt the auto-generated ViewSets and Serializers to
# Django at runtime using the setattr() method.

"""
This function generates serializers for every model returned in apps.apps.get_models()
Adjusting the `depth` variable on Meta class can drastically speed up the API.
It's recommended to use a customer Manager on each of your models to override
`select_related` and `prefetch_related` and define which fields need joined there.
"""
def listMethods():
    return ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
def make_api_serializers(api_models, base_serializer_class=serializers.ModelSerializer):
    api_serializers = []
    for ModelClass in api_models:
        class_name = f'{ModelClass.__name__}Serializer'
        exclude_fields_for_methods = {
            "POST": ('id',), #validate_id is not working, so we will just use this one here
            "GET": (),
            "PUT": (),
            "PATCH": (),
            "DELETE": (),
        }
        methods = listMethods()
        methods_serializers = {}
        for method in methods:
            def getModelSerializer(ModelClass, method):
                class_name = f'{ModelClass.__name__}Serializer'
                class ModelSerializer(base_serializer_class):
                    class Meta:
                        model = ModelClass
                        depth = 10
                        if exclude_fields_for_methods[method]:
                            exclude = exclude_fields_for_methods[method]
                        else:
                            fields = '__all__'
                    def validate_id(self, value):
                        if self.context['request'].method == 'POST' and value is not None:
                            raise serializers.ValidationError("Cannot specify 'id' when creating a new object.")
                        return value
                
                ModelSerializer.__name__ = class_name
                return ModelSerializer
            methods_serializers[method] = getModelSerializer(ModelClass, method)
        api_serializers.append({f"{ModelClass._meta.app_label}.{ModelClass.__name__}": methods_serializers})
    return api_serializers

auto_apps_models = [model for model in apps.apps.get_models() if hasattr(model, 'autoLoad') and model.autoLoad]
api_serializers = make_api_serializers(auto_apps_models)

for ser in api_serializers:
   name = tuple(ser.keys())
   setattr(module, name[0].lower(), ser[name[0]])

"""
This function generates ModelViewSets for every model returned in apps.apps.get_models()
and zips in all the api_serializers models generated in previous for-loop.
"""
def make_api_viewsets(api_models, api_serializers):
    api_viewsets = []
    for ModelClass, SerializerClass in zip(api_models, api_serializers):
        table_name = ModelClass._meta.db_table
        app_name = ModelClass._meta.app_label       
        def create_viewset(ModelClass, table_name, SerializerClass):
            class ModelViewSet(viewsets.ModelViewSet):
                db_table =  table_name
                queryset = ModelClass.objects.all()
                app_name = ModelClass._meta.app_label

                def get_serializer_class(self):
                    method = self.request.method

                    serializer = SerializerClass[f'{self.app_name}.{ModelClass.__name__}'].get(method)
                    # get valid data here
                    
                    if serializer is None:
                        raise ValueError(f"No serializer defined for method {method}")
                    return serializer

            return ModelViewSet
        viewset = create_viewset(ModelClass, table_name, SerializerClass)
        api_viewsets.append({f"{app_name}.{ModelClass.__name__}": viewset})
    return api_viewsets

api_viewsets = make_api_viewsets(auto_apps_models, api_serializers)

for vs in api_viewsets:
   name = tuple(vs.keys())
   setattr(module, name[0].lower(), vs[name[0]])

# Creates a list of tuples that is used to then register generated ModelViewSets in DRF.
# The router is imported into the main urls.py file and uses include('router.urls') within
# the urlpatters list that Django loads at runtime. See the README for more info.
rest_api_urls = []
for viewset in api_viewsets:
    app_name = list(viewset.keys())[0].lower().split('.')
    k = list(viewset.keys())[0]
    rest_api_urls.append((fr'{app_name[0]}/{app_name[1]}', viewset[k], f'{app_name[0]}/{app_name[1]}'))

router = routers.DefaultRouter()
for route in rest_api_urls:
    router.register(route[0], route[1], basename=route[2])