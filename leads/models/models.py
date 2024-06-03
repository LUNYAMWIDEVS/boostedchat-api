from django.db import models

# Create your models here
from base.models import BaseModel
from instagram.models import Account
from sales_rep.models import SalesRep, SalesRepProfileList
from channels.models import Channel, ChannelActivity


# Create your models here.
class Lead(BaseModel):
    instagram = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)


class Leads(models.Model):
    name = models.CharField(max_length=255,  null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    score = models.FloatField(default=0.0) # overall after evaluating for each sales-rep
    # leadSalesRepScore = models.ManyToManyField(SalesRep, through='LeadScore')
    def __str__(self):
        return f"{self.name} - Score: {self.score}"

# class LeadScore(models.Model):
#     lead = models.OneToOneField(Leads, on_delete=models.CASCADE)
#     score = models.FloatField(default=0.0) # overall after evaluating for each sales-rep

#     def __str__(self):
#         return f"{self.lead.name} - Score: {self.score}"

class LeadScore(models.Model):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)
    # sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)
    sales_rep_profiles = models.ManyToManyField(SalesRepProfileList)
    score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.lead.name} assigned to {self.sales_rep_profiles} - {self.score}%"
    
class LeadOutreachTrial(models.Model):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)
    trial_number = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('lead', 'sales_rep', "trial_number")

    def __str__(self):
        return f"{self.lead.name} assigned to {self.sales_rep.full_name} - {self.trial_number}"

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





    

    # def __str__(self):
    #     return f"{self.lead_outreach_trial.lead.name} assigned to {self.lead_outreach_trial.sales_rep.full_name} - {self.activity}"

class LeadChannel(models.Model):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        unique_together = ('lead', 'channel')

    def __str__(self):
        return f"{self.lead.name} assigned to {self.channel.name} as {self.username}"


class LeadsManager(models.Manager):
    def get_queryset(self):
        return Leads.objects.all()#.filter(status='active')
    def get_leads(self):
        return self.get_queryset()
    def create_lead(self, lead_name=None):
        lead = Leads.objects.create(lead_name=lead_name)
        return lead
     # not yet implemented
    def create_lead_for_channel(self, channel_name=None, lead_name=None):
        lead = Leads.objects.create(lead_name=lead_name)
        return lead
   
    def add_channel_to_lead(self, channel_name=None, lead_name=None):
        lead = Leads.objects.create(lead_name=lead_name)
        return lead