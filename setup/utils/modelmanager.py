from base.models import BaseModel
from django.db.models import Q
from rest_framework import serializers
from django.db import IntegrityError
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField, ManyToOneRel, OneToOneRel


class modelManager(models.Manager):
    class Meta:
        app_label = 'setup'  # Replace 'your_app_label' with the actual app label

    def __init__(self, model):
        self.localModel = model

    def create_dynamic_serializer(self, model, extra_fields = {}, redacted_fields = []):
        model_fields, _,required_fields, _ = self.getModelFields(model)
        # Create a base serializer class
        class DynamicSerializer(serializers.ModelSerializer):
            class Meta:
                model = None
                # fields = '__all__'
                depth = 2
                exclude = []
        DynamicSerializer.Meta.model = model 
        DynamicSerializer.Meta.exclude = ['id'] 
        
        return DynamicSerializer
        for field_name, field in model_fields.items():            
            if isinstance(field, (ForeignKey, ManyToManyField, OneToOneField, ManyToOneRel, OneToOneRel)):
                # Handle relationship fields using appropriate serializer fields
                if isinstance(field, ForeignKey):
                    serializer_field = serializers.PrimaryKeyRelatedField(queryset=field.related_model.objects.all(), required=False)
                elif isinstance(field, ManyToManyField):
                    serializer_field = serializers.PrimaryKeyRelatedField(queryset=field.related_model.objects.all(), required=False, many=True)
                elif isinstance(field, OneToOneField):
                    serializer_field = serializers.PrimaryKeyRelatedField(queryset=field.related_model.objects.all(), required=False)
                elif isinstance(field, ManyToOneRel):
                    serializer_field = serializers.PrimaryKeyRelatedField(queryset=field.related_model.objects.all(), required=False, many=True)
                elif isinstance(field, OneToOneRel):
                    serializer_field = serializers.PrimaryKeyRelatedField(queryset=field.related_model.objects.all(), required=False)
                # setattr(DynamicSerializer, field_name, serializer_field)
            else:
                try:
                    serializer_field = self.get_serializer_field(field)
                    print("serializer_field", serializer_field, field_name, field, required_fields)
                except:
                    continue

            setattr(DynamicSerializer, field_name, serializer_field)

        # Dynamically create extra fields
        for field_name, field_info in extra_fields.items():
            if field_info["type"] in serializers.FIELD_CLASSES:  # Check if the field type is valid
                serializer_field = field_info["type"](required=field_info["required"])
                setattr(DynamicSerializer, field_name, serializer_field)
        # Dynamically remove redacted fields
        for field_name in redacted_fields:
            if field_name in model_fields:
                delattr(DynamicSerializer, field_name)
        print(DynamicSerializer)
        print(dir(DynamicSerializer))
        return DynamicSerializer
    
    def get_serializer_field(self, field):
        """
        Get the appropriate serializer field based on the model field.
        """
        field_class = serializers.CharField  # Default to CharField

        if isinstance(field, models.IntegerField):
            field_class = serializers.IntegerField
        elif isinstance(field, models.FloatField):
            field_class = serializers.FloatField
        elif isinstance(field, models.BooleanField):
            field_class = serializers.BooleanField
        elif isinstance(field, models.DateField):
            field_class = serializers.DateField
        elif isinstance(field, models.DateTimeField):
            field_class = serializers.DateTimeField
        elif isinstance(field, models.DecimalField):
            field_class = serializers.DecimalField
        elif isinstance(field, models.EmailField):
            field_class = serializers.EmailField
        elif isinstance(field, models.URLField):
            field_class = serializers.URLField
        elif isinstance(field, models.ImageField):
            field_class = serializers.ImageField
        elif isinstance(field, models.FileField):
            field_class = serializers.FileField
        elif isinstance(field, models.UUIDField):
            field_class = serializers.UUIDField
        elif isinstance(field, models.DurationField):
            field_class = serializers.DurationField
        return field_class(required=not field.null, allow_null=field.null)
    
    def getDynamicSerializer(self, action, extra_fields = {}, redacted_fields = []):
        redacted_fields = redacted_fields + ['id'] if action == 'create' else redacted_fields # remove id field for create action
        return self.create_dynamic_serializer(self.localModel, extra_fields, redacted_fields)

    def getModelFields(self, model):
        # filters = Q()
        # model_fields = {field.name for field in model._meta.get_fields()}  # Get model field names
        model_fields = {field.name: field for field in model._meta.get_fields()} 
        unique_fields = [field.name for field in model._meta.get_fields() if getattr(field, 'unique', False)]
        required_fields = [field.name for field in model._meta.get_fields() if getattr(field, 'null', False) == False]
        primary_key = model._meta.pk.name
        return (model_fields, unique_fields, required_fields, primary_key)
    
    def uniqueFieldsExist(self, model, params = {}):
        model_fields, unique_fields,_, primary_key = self.getModelFields(model)
        filters = Q()
        for field, value in params.items():
            if (field in unique_fields  or field == primary_key) and value is not None:
                filters |= Q(**{field: value})
        return model.objects.filter(filters).exists()
    
    # get from params only the fields which are in model_fields
    def model_field_params(self, model, params={}):
        model_fields = {field.name for field in model._meta.get_fields()}  # Get model field names
        valid_params = {key: value for key, value in params.items() if key in model_fields}
        return valid_params


    def save_model(self, params = {}, semi_primary_key = None): # semi_primary is the unique field to filter by
        if self.uniqueFieldsExist(self.localModel, params):
            raise serializers.ValidationError(f"Record already exists.")
       
        valid_params = self.model_field_params(self.localModel, params)
        recordExists = False
        record_is_deleted = False
        if semi_primary_key is not None:
            semi_primary_value = valid_params[semi_primary_key]
            recordExists = self.localModel.objects.filter(semi_primary_key=semi_primary_value ).exists()
            record_is_deleted = self.localModel.objects.all_with_deleted().filter(semi_primary_key=semi_primary_value).exists()
        if record_is_deleted:
            self.ChannelUserNames.objects.all_with_deleted().filter(semi_primary_key=semi_primary_value).first().undelete()
        local_entry = None
        try:
            local_entry, created = self.localModel.objects.get_or_create(
                valid_params
            )
            # Update existing record if not created
            if not created:
                for field, value in valid_params.items():
                    setattr(local_entry, field, value)
                local_entry.save()
        except IntegrityError as e:
                if recordExists:
                    raise serializers.ValidationError(f"Record already exists.")
                else:
                    raise serializers.ValidationError(f"Unknown erorr for record")

        return local_entry

    
    # def read_model(self, params = {}):
    #     """
    #     Reads usernames based on the provided parameters. Filters based on any non-None parameter present in the ChannelUserNames model.

    #     Args:
    #         params (dict, optional): A dictionary containing optional filter parameters.
    #             Defaults to {}.

    #     Returns:
    #         QuerySet: A queryset of ChannelUserNames objects filtered based on the params.
    #     """
    #     filters = Q()
    #     model_fields = {field.name for field in self.ChannelUserNames._meta.get_fields()}  # Get model field names
    #     for field, value in params.items():
    #         if value is not None and field in model_fields:  # Check for non-None value and valid field
    #             filters &= Q(**{field: value})
    #     return self.ChannelUserNames.objects.filter(filters)
    


    # def update_model(self, params = {}):
    #     _, _, username, status1, status2, status3, sandbox, filters = helpers.getChannelUserNameParams(params, action="update")
    #     channel_usernames = self.read_channel_usernames(filters) # user filters here
    #     for channel_username in channel_usernames:
    #         if channel_username:
    #             model_fields = {field.name for field in self.ChannelUserNames._meta.get_fields()}  # Get model field names
    #             for field, value in params.items():
    #                 if value is not None and field in model_fields:  # Check for non-None value and valid field
    #                     setattr(channel_username, field, value)
    #             channel_username.save()
    #     return channel_usernames

    # def delete_model(self, params = {}):
    #     _, id, _, _, _, _, _, filters = helpers.getChannelUserNameParams(params)
    #     channel_username = self.read_channel_username(filters)
    #     channel_usernames = self.read_channel_usernames(filters) # user filters here
    #     for channel_username in channel_usernames:
    #         if channel_username:
    #             channel_username.delete()
    #     return False
