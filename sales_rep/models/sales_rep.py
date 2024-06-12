from django.db import models

from authentication.models import User
from base.models import BaseModel
from instagram.models import Account
from setup.utils import setuputils
from setup.utils import modelManager
from channels.models.channels import Channel, ChannelActivity
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import serializers

# from leads.models.models import LeadOutreachTrial, LeadOutreachActivities

class SalesRep(BaseModel):
    autoLoad = True
    permissionClasses = [IsAuthenticatedOrReadOnly]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    ig_username = models.CharField(max_length=255, null=True, blank=True) # backward compartibility
    ig_password = models.CharField(max_length=255, null=True, blank=True) # backward compartibility
    instagram = models.ManyToManyField(Account, blank=True) # backward compartibility
    available = models.BooleanField(default=True) # backward compartibility
    country = models.TextField(default="US")
    city = models.TextField(default="Pasadena")

    def __str__(self) -> str:
        return self.user.email
    
# All Channels Registered to sales_rep, with their credentials where applicable
class SalesRepChannel(models.Model):
    autoLoad = True
    permissionClasses = [IsAuthenticated]
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=True, blank=True)  
    password = models.CharField(max_length=255, null=True, blank=True)
    available = models.BooleanField(default=True) 
    start_time = models.TimeField()
    end_time = models.TimeField()
    # max_capacity = models.IntegerField(default=0)
    timezone = models.CharField(max_length=255)
    sandbox = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sales_rep', 'channel')

    def __str__(self):
        return f"{self.sales_rep}({self.sales_rep.full_name}) on {self.channel}"

## this is required so that we can be able to define the working hours per activity
class SalesRepChannelActivity(models.Model): # all the activities which a sales_rep can do
    autoLoad = True
    permissionClasses = [IsAuthenticated]
    # sales_rep_channel = models.ForeignKey(SalesRepChannel, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE) # use this instead of sales_rep_channel
    activity = models.ForeignKey(ChannelActivity, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True, blank=True) # if this is not defined, we will use for SalesRepChannel
    end_time = models.TimeField(null=True, blank=True) # if this is not defined, we will use for SalesRepChannel
    available = models.BooleanField(default=True) # if this is not defined, we will use for SalesRepChannel
    max_capacity = models.IntegerField(default=0) 
    # timezone = models.CharField(max_length=255) # we will use for SalesRepChannel
    # class Meta:
    #     unique_together = ('sales_rep_channel', 'activity')

    def __str__(self):
        return f"{self.sales_rep}: {self.activity}"
    
# # salesRep activity capacities
# class SalesRepChannelActivityCapacity(models.Model):
#     autoLoad = True
#     permissionClasses = []
#     sales_rep_channel = models.ForeignKey(SalesRepChannel, on_delete=models.CASCADE)
#     activity = models.ForeignKey(ChannelActivities, on_delete=models.CASCADE)
#     max_capacity = models.IntegerField()

#     class Meta:
#         unique_together = ('sales_rep_channel', 'activity')

#     def __str__(self):
#         return f"{self.sales_rep} on {self.channel}"

# Records each shift
class SalesRepWorkingShiftManager(modelManager):
    def __init__(self, model):
        self.model = model
        super().__init__(model)
    # create salesRep... does it create a new user??
    def save_model(self, params = {}):
        # set all active for sales_rep to False
        sales_rep = params.get("sales_rep")
        channel = params.get("channel")
        # get records for sales_rep and channel
        records = self.model.objects.filter(sales_rep=sales_rep, channel=channel)
        for record in records:
            record.active = False
            record.save()
        return super().save_model(params)

class WorkingShiftsSerializer(serializers.Serializer):
        sales_rep = serializers.CharField(required=True)
        channel = serializers.IntegerField(required=True)
        # shift_number = serializers.IntegerField(required=False) # What is the need for this? Just get the last shift for channel
        start_time = serializers.TimeField(required=True)
        end_time = serializers.TimeField(required=True)
        active = serializers.BooleanField(required=False, default=True)

class SalesRepsChannelWorkingShift(models.Model):
    autoLoad = True
    permissionClasses = []
    modelManager = SalesRepWorkingShiftManager
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    # shift_number = models.IntegerField() # what is the need for this? Just get the last shift for channel
    # shift_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    active = models.BooleanField(default=True)

    localSerializers = {
        "WorkingShiftsSerializer":{
            "methods": ["POST"],
            "serializer": WorkingShiftsSerializer
        }
    }

    # unique_together = ('sales_rep', 'channel', 'shift_number')

    def __str__(self):
        return f"{self.id} of {self.sales_rep} on {self.channel}"
    
# # Records the activity done in each shift
# class SalesRepChannelWorkingShiftActivity(models.Model):
#     autoLoad = True
#     permissionClasses = [IsAuthenticated]
#     sales_rep_channel_shift = models.ForeignKey(SalesRepsChannelWorkingShift, on_delete=models.CASCADE)
#     activity = models.ForeignKey(SalesRepChannelActivity, on_delete=models.CASCADE)
#     lead_outreach_activity = models.ForeignKey(LeadOutreachActivities, on_delete=models.CASCADE, null=True, blank=True)
#     def __str__(self):
#         return f"{self.sales_rep} on {self.channel}"

class SalesRepProfileList(models.Model):
    autoLoad = True
    permissionClasses = [IsAuthenticated]
    profile = models.TextField(unique=True)

    def __str__(self):
        return f"{self.profile}"
        
class SalesRepProfile(models.Model):
    autoLoad = True
    permissionClasses = [IsAuthenticated]
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)
    profile = models.ManyToManyField(SalesRepProfileList)
    # class Meta:
    #     unique_together = ('sales_rep', 'profile')

    def __str__(self):
        return f"{self.sales_rep}: {self.profile}"

## This should be per activity
##
class SalesRepChannelRunningAverage(models.Model): 
    autoLoad = True
    permissionClasses = [IsAuthenticated]
    sales_rep_channel_activity = models.ForeignKey(SalesRepChannelActivity, on_delete=models.CASCADE)
    date = models.DateField()
    average = models.IntegerField() # should increase daily but not be more than max_capacity

## WorkingShiftErrors: record errors encountered for each activity during a shift
class SalesRepChannelWorkingShiftError(models.Model):
    autoLoad = True
    permissionClasses = [IsAuthenticated]
    sales_rep_channel_shift = models.ForeignKey(SalesRepsChannelWorkingShift, on_delete=models.CASCADE)
    message = models.TextField()
    code = models.IntegerField()
    level = models.IntegerField(default=0) # 0: info, 0: warning, 1: error

    

salesRepModelManager = modelManager(SalesRep)
# create salesRepManager. Refer for channels/models/channels.py
class SalesRepManager(modelManager):
    def __init__(self):
        super().__init__(SalesRep)
    # create salesRep... does it create a new user??
    def save_sales_rep(self, params = {}):
        print("params", params)
        return self.save_model(params)
        
    def get_queryset(self):
        return SalesRep.objects.all()

    def get_sales_reps(self):
        return self.get_queryset()

    def create_sales_rep(self, user=None, ig_username=None, ig_password=None, instagram=None, available=None, country=None, city=None):
        sales_rep = SalesRep.objects.create(user=user, ig_username=ig_username, ig_password=ig_password, instagram=instagram, available=available, country=country, city=city)
        return sales_rep

    def update_sales_rep(self, user=None, ig_username=None, ig_password=None, instagram=None, available=None, country=None, city=None):
        sales_rep = SalesRep.objects.get(user=user)
        if sales_rep:
            sales_rep.ig_username = ig_username
            sales_rep.ig_password = ig_password
            sales_rep.instagram = instagram
            sales_rep.available = available
            sales_rep.country = country
            sales_rep.city = city
            sales_rep.save()
            return True
        return False

    def delete_sales_rep(self, user=None):
        sales_rep = SalesRep.objects.get(user=user)
        if sales_rep:
            sales_rep.delete()
            return True
        return False

    def get_sales_rep(self, user=None):
        return SalesRep.objects.get(user=user)

    def get_sales_rep_by_ig_username(self, ig_username=None):
        return SalesRep.objects.get(ig_username=ig_username)

    def get_sales_rep_by_ig_password(self, ig_password=None):
        return SalesRep.objects.get(ig_password=ig_password)

    def get_sales_rep_by_instagram(self, instagram=None):
        return SalesRep.objects.get(instagram=instagram)

    def get_sales_rep_by_available(self, available=None):
        return SalesRep.objects.get(available=available)

    def get_sales_rep_by_country(self, country=None):
        return SalesRep.objects.get(country=country)

    def get_sales_rep_by_city(self, city=None):
        return SalesRep.objects.get(city=city)
