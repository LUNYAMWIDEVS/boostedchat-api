from django.db import models

# Create your models here
from base.models import BaseModel
from instagram.models import Account
from sales_rep.models import SalesRep, SalesRepProfileList
from channels.models import Channel, ChannelActivity
from rest_framework import serializers

# Create your models here.
class Lead(BaseModel):
    instagram = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)


class Leadv1(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    autoLoad = True
    permissionClasses = []
    name = models.CharField(max_length=255,  null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    score = models.FloatField(default=0.0) # overall after evaluating for each sales-rep
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='active',
    )
    # leadSalesRepScore = models.ManyToManyField(SalesRep, through='LeadScore')
    def __str__(self):
        return f"{self.id}: {self.name} - Score: {self.score}"

class LeadScore(models.Model): # todo: check: not working yet
    autoLoad = True
    permissionClasses = []
    lead = models.ForeignKey(Leadv1, on_delete=models.CASCADE)
    sales_rep_profiles = models.ManyToManyField(SalesRepProfileList)
    score = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.lead.name} assigned to {self.sales_rep_profiles} - {self.score}%"
    
class LeadChannelSerializer(serializers.Serializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Leadv1.objects.all())
    channel = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all())
    username = serializers.CharField(max_length=255, required=False)

    def create_new_lead(self):
        lead = Leadv1.objects.create()
        return lead
    
    def create(self, validated_data): # we will assume that lead exists
        lead_data = validated_data.get('lead')
        
        if isinstance(lead_data, Leadv1):
            id = lead_data.__dict__["id"]
            if id == 1:
                lead = self.create_new_lead()
                validated_data['lead'] = lead        
        return LeadChannel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.lead = validated_data.get('lead', instance.lead)
        instance.channel = validated_data.get('channel', instance.channel)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
    
class LeadChannel(models.Model):
    autoLoad = True
    permissionClasses = []
    localSerializers = {
        "WorkingShiftsSerializer":{
            "methods": ["POST"],
            "serializer": LeadChannelSerializer
        }
    }
    lead = models.ForeignKey(Leadv1, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        unique_together = ('lead', 'channel')

    def __str__(self):
        return f"{self.lead.id}:{self.lead.name} assigned to {self.channel.name} as {self.username}"
    
class LeadOutreachTrialSerializer(serializers.Serializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Leadv1.objects.all())
    sales_rep = serializers.PrimaryKeyRelatedField(queryset=SalesRep.objects.all())
    # trial_number = serializers.IntegerField(default=0)
    # active = serializers.BooleanField(default=True)
    force = serializers.BooleanField(default=False)

    def create(self, validated_data):
        trials = LeadOutreachTrial.objects.filter(sales_rep=validated_data.get('sales_rep'), lead=validated_data.get('lead'))
        trial_number = 0
        if trials.exists():
            trial_number = trials.last().trial_number + 1
        # put trial_number in validated_data
        validated_data['trial_number'] = trial_number
        if not validated_data.get('force', False):
            active_trial = LeadOutreachTrial.objects.filter(sales_rep=validated_data.get('sales_rep'), lead=validated_data.get('lead'), active=True)
            if active_trial.exists():
                return active_trial.first()
            else:
                del validated_data['force']
                return LeadOutreachTrial.objects.create(**validated_data)
        else:
            # delete force from validated_data
            del validated_data['force']
            # we will need to set all existing records to inactive
            active_trial = LeadOutreachTrial.objects.filter(sales_rep=validated_data.get('sales_rep'), lead=validated_data.get('lead'), active=True)
            if active_trial.exists():
                active_trial.update(active=False)
            return LeadOutreachTrial.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.lead = validated_data.get('lead', instance.lead)
        instance.sales_rep = validated_data.get('sales_rep', instance.sales_rep)
        instance.trial_number = validated_data.get('trial_number', instance.trial_number)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
class LeadOutreachTrial(models.Model):
    autoLoad = True
    permissionClasses = []
    localSerializers = {
        "LeadOutreachTrialSerializer":{
            "methods": ["POST"],
            "serializer": LeadOutreachTrialSerializer
        }
    }
    lead = models.ForeignKey(Leadv1, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)
    trial_number = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('lead', 'sales_rep', "trial_number")

    def __str__(self):
        return f"{self.lead.name} assigned to {self.sales_rep.full_name} - {self.trial_number}"
    
'''
Remodeling how to handle outreach activities
'''
class ActivitySerializer(serializers.Serializer):
    trial = serializers.PrimaryKeyRelatedField(queryset=LeadOutreachTrial.objects.all())
    content = serializers.CharField(max_length=255)
    activity = serializers.PrimaryKeyRelatedField(queryset=ChannelActivity.objects.all())

    def create(self, validated_data):
        # we need to run the checks here
        return LeadActivity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.trial = validated_data.get('trial', instance.trial)
        instance.content = validated_data.get('content', instance.content)
        instance.activity = validated_data.get('activity', instance.activity)
        instance.save()
        return instance

class LeadActivity(models.Model):
    autoLoad = True
    permissionClasses = []
    localSerializers = {
        "ActivitySerializer":{
            "methods": ["POST"],
            "serializer": ActivitySerializer
        }
    }
    trial = models.ForeignKey(LeadOutreachTrial, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    activity= models.ForeignKey(ChannelActivity, on_delete=models.CASCADE)
    def __str__(self):
        return self.content

class Error(models.Model):
    error_message = models.CharField(max_length=255)
    # Additional fields for error

# class Status(models.Model):
#     status_message = models.CharField(max_length=255)
#     # Additional fields for status

class Message(models.Model):
    content = models.CharField(max_length=255)

class LeadOutreachActivities(models.Model):
    lead_outreach_trial = models.ForeignKey(LeadOutreachTrial, on_delete=models.CASCADE)
    channel_activity = models.ForeignKey(ChannelActivity, on_delete=models.CASCADE)
    error = models.ForeignKey(Error, on_delete=models.SET_NULL, null=True, blank=True)
    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        FAILURE = 'failure', 'Failure'
        SCHEDULED = 'scheduled', 'Scheduled'
        RECEIVED = 'received', 'Received'
    status = models.CharField(max_length=255, default='scheduled')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)




class LeadsManager(models.Manager):
    def get_queryset(self):
        return Leadv1.objects.all()#.filter(status='active')
    def get_leads(self):
        return self.get_queryset()
    def create_lead(self, lead_name=None):
        lead = Leadv1.objects.create(lead_name=lead_name)
        return lead
     # not yet implemented
    def create_lead_for_channel(self, channel_name=None, lead_name=None):
        lead = Leadv1.objects.create(lead_name=lead_name)
        return lead
   
    def add_channel_to_lead(self, channel_name=None, lead_name=None):
        lead = Leadv1.objects.create(lead_name=lead_name)
        return lead