from django.db import models
from base.models import BaseModel
from sales_rep.models import SalesRep
from leads.models import Leads
from channels.models.helpers import *
from setup.utils import modelManager
from rest_framework import serializers


class IGManager (modelManager):
    # def __init__(self):
    #     pass

    def save_model(self, *args, **kwargs):
        return super().save_model(*args, **kwargs)
        
class ChannelUserNameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True) # username to be saved
    status1 = serializers.CharField(required=False)
    status2 = serializers.CharField(required=False)
    status3 = serializers.CharField(required=False)
    status4 = serializers.CharField(required=False)
    sandbox = serializers.BooleanField(required=False, allow_null=True, default=None) # we do not want this to defaul to False

# /GET with channel
class ChannelUserNameFilterSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    status1 = serializers.CharField(required=False)
    status2 = serializers.CharField(required=False)
    status3 = serializers.CharField(required=False)
    status4 = serializers.CharField(required=False)
    sandbox = serializers.BooleanField(required=False)

# Model to track Instagram usernames and their status
class InstagramUserNames(BaseModel):
    autoLoad = True
    permissionClasses = []
    modelManager = IGManager
    localSerializers = {
        "ChannelUserNameSerializer": {
            "serializer": ChannelUserNameSerializer,
            "methods": ["POST", "DEFAULT"] # Default is not in use now. it will default to method serializer for api_generator
        },
         "ChannelUserNameFilterSerializer": {
            "serializer": ChannelUserNameFilterSerializer,
            "methods": ["GET", "PUT"]
        }
    }
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    status1 = models.CharField(max_length=255, null=True, blank=True)
    status2 = models.CharField(max_length=255, null=True, blank=True)
    status3 = models.CharField(max_length=255, null=True, blank=True)
    # status4 = models.CharField(max_length=255, null=True, blank=True)
    sandbox = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.username

# These usernames will not be run on the real social media platform
class InstagramSandboxUserNames(BaseModel):
    instagram_username = models.ForeignKey(InstagramUserNames, on_delete=models.CASCADE)

    def __str__(self):
        return self.instagram_username.username

# Model to track historical usernames for leads
class InstagramLeadUserNames(BaseModel):
    instagram_username = models.ForeignKey(InstagramUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track current username for leads
class InstagramLead(BaseModel):
    instagram_username = models.ForeignKey(InstagramLeadUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track historical usernames for sales representatives
class InstagramSalesRepUserNames(BaseModel):
    instagram_username = models.ForeignKey(InstagramUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

# Model to track current username for sales representatives
class InstagramSalesRep(BaseModel):
    instagram_username = models.ForeignKey(InstagramSalesRepUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

"""

Sales_Rep
    |
    |------InstagramSalesrep
    |                |
    |                \|/
    |------InstagramLeadUserNames

# same for lead
"""


