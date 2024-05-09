from rest_framework import serializers
from channels.models import *
class ChannelUserNameSerializer(serializers.Serializer):
     channel = serializers.CharField(required=True)
     username = serializers.CharField(required=False)
     status1 = serializers.CharField(required=False)
     status2 = serializers.CharField(required=False)
     status3 = serializers.CharField(required=False)
     status4 = serializers.CharField(required=False)
     sandbox = serializers.BooleanField(required=False, allow_null=True, default=None) # we do not want this to defaul to False

     def validate(self, data):
        """
        Validate the serializer data.
        """
        channel = data.get('channel')
        username = data.get('username')
        status1 = data.get('status1')
        status2 = data.get('status2')
        status3 = data.get('status3')
        status4 = data.get('status4')
        sandbox = data.get('sandbox')

        channel = channel.lower()
        data["channel"]= channel
        if channel not in helpers.channelsList():
            raise serializers.ValidationError("Channel must be one of the following: " + str(helpers.channelsList()))
        return data
class ChannelUserNamesReadSerializer(serializers.Serializer):
     id = serializers.CharField(required=False)
     username = serializers.CharField(required=False)
     status1 = serializers.CharField(required=False)
     status2 = serializers.CharField(required=False)
     status3 = serializers.CharField(required=False)
     status4 = serializers.CharField(required=False)
     sandbox = serializers.BooleanField(required=False)
     created_at = serializers.DateTimeField(required=False)
     updated_at = serializers.DateTimeField(required=False)
     deleted_at = serializers.DateTimeField(required=False)

     def validate(self, data):
        """
        Validate the serializer data.
        """
        username = data.get('username')
        status1 = data.get('status1')
        status2 = data.get('status2')
        status3 = data.get('status3')
        status4 = data.get('status4')
        sandbox = data.get('sandbox')
        return data
     
# from rest_framework import serializers
# from .models import InstagramUserNames, InstagramSandboxUserNames

# class InstagramUserNamesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstagramUserNames
#         fields = '__all__'

# class InstagramSandboxUserNamesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstagramSandboxUserNames
#         fields = '__all__'

