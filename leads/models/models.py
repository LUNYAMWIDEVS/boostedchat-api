from django.db import models

# Create your models here
from base.models import BaseModel
from instagram.models import Account


# Create your models here.
class Lead(BaseModel):
    instagram = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)


class Leads(BaseModel):
    lead_name = models.CharField(max_length=255, null=True, blank=True)

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