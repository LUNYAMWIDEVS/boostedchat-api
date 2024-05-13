from rest_framework import serializers
from channels.models import *

class ChannelSSerializer(serializers.Serializer):
    channel = serializers.CharField(required=True)  # select the channel

    def validate_channel(self, value):
        """
        Validate the 'channel' field.
        """
        channel = value.lower()
        if channel not in helpers.channelsList():
            raise serializers.ValidationError("Channel must be one of the following: " + str(helpers.channelsList()))
        return channel

# /POST with channel
class ChannelUserNameSerializer(ChannelSSerializer):
    username = serializers.CharField(required=True) # username to be saved
    status1 = serializers.CharField(required=False)
    status2 = serializers.CharField(required=False)
    status3 = serializers.CharField(required=False)
    status4 = serializers.CharField(required=False)
    sandbox = serializers.BooleanField(required=False, allow_null=True, default=None) # we do not want this to defaul to False

# /GET with channel
class ChannelUserNameFilterSerializer(ChannelSSerializer):
    id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    status1 = serializers.CharField(required=False)
    status2 = serializers.CharField(required=False)
    status3 = serializers.CharField(required=False)
    status4 = serializers.CharField(required=False)
    sandbox = serializers.BooleanField(required=False, allow_null=True, default=None) # we do not want this to defaul to False

# /PATCH with channel
class ChannelUserNamePatchSerializer(ChannelSSerializer):
    channel = serializers.CharField(required=True)
    username = serializers.CharField(required=False)
    status1 = serializers.CharField(required=False)
    status2 = serializers.CharField(required=False)
    status3 = serializers.CharField(required=False)
    status4 = serializers.CharField(required=False)
    sandbox = serializers.BooleanField(required=False, allow_null=True, default=None) # we do not want this to default to False
    filters = serializers.JSONField(required=True)

    def validate_filters(self, value):
        expected_keys = ['id', 'channel', 'username', 'status1', 'status2', 'status3', 'status4', 'sandbox']
        # Check if filters is empty
        if not value:
            raise serializers.ValidationError("filters must not be empty")

        # Check if any expected key is in the value
        if not any(key in value for key in expected_keys):
            raise serializers.ValidationError("filters must contain any of the following keys: {}".format(', '.join(expected_keys)))

        return value
    
    def validate_channel(self, value):
        channel = value.lower()
        if channel not in helpers.channelsList():
            raise serializers.ValidationError("Channel must be one of the following: " + str(helpers.channelsList()))
        return channel

# For reading channel usernames for /GET and /PATCH (response)
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

# for deleting a channel username: /DELETE
class ChannelUserNameDeleteSerializer(ChannelSSerializer):
    id = serializers.CharField(required=True)

     
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

