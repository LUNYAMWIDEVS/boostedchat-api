# from rest_framework import serializers

# def create_dynamic_serializer(model_fields):
#     # Create a base serializer class
#     class DynamicSerializer(serializers.Serializer):
#         pass

#     # Dynamically create serializer fields based on model_fields
#     for field_name, field_type in model_fields.items():
#         serializer_field = field_type(required=False)  # Assuming all fields are optional
#         setattr(DynamicSerializer, field_name, serializer_field)

#     return DynamicSerializer