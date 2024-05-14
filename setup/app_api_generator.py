# ref: https://gist.github.com/D2theR/0b439164e94a9577d4b502496c7672cf
"""
Auto-generates Serializers & ModelViewSets in a Django API using just models
Adjusted to include only the apps that have auto settings enabled in settings.py
"""
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
def make_api_serializers(api_models, base_serializer_class=serializers.ModelSerializer):
    api_serializers = []
    for ModelClass in api_models:
        #Create the serializer class
        class_name = f'{ModelClass.__name__}Serializer'
        class ModelSerializer(base_serializer_class):
            class Meta:
                model = ModelClass
                fields = '__all__'
                depth = 2
        ModelSerializer.__name__ = class_name
        api_serializers.append({f"{ModelClass._meta.app_label}.{ModelClass.__name__}" :ModelSerializer})
    return api_serializers



"""
This function generates ModelViewSets for every model returned in apps.apps.get_models()
and zips in all the api_serializers models generated in previous for-loop.
"""
def make_api_viewsets(api_models, api_serializers):
    api_viewsets = []
    for ModelClass, SerializerClass in zip(api_models, api_serializers):
        table_name = ModelClass._meta.db_table
        app_name = ModelClass._meta.app_label
        viewset_name = f'{ModelClass.__name__}ViewSet'
        viewset_bases = (viewsets.ModelViewSet,)
        viewset_attrs = {
            'db_table': table_name,
            'queryset': ModelClass.objects.all(),
            'serializer_class': SerializerClass[f'{app_name}.{ModelClass.__name__}'],
            'app_name': app_name
        }

        ModelViewSet = type(
            viewset_name,
            viewset_bases,
            viewset_attrs,
        )
        api_viewsets.append({f"{app_name}.{ModelClass.__name__}" :ModelViewSet})
    return api_viewsets

auto_apps_models = [model for model in apps.apps.get_models() if hasattr(model, 'autoLoad') and model.autoLoad]

api_serializers = make_api_serializers(auto_apps_models)

for ser in api_serializers:
   name = tuple(ser.keys())
   setattr(module, name[0].lower(), ser[name[0]])
api_viewsets = make_api_viewsets(auto_apps_models, api_serializers)


for vs in api_viewsets:
   print(vs)
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
    print(route[0], route[1], route[2])
    router.register(route[0], route[1], basename=route[2])