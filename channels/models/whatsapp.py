from django.db import models
from base.models import BaseModel
from sales_rep.models import SalesRep
from leads.models import Leads
from. import helpers
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly

# Model to track Whatsapp usernames and their status
class WhatsappUserNames(BaseModel):
    autoLoad = True
    permissionClasses = [IsAuthenticatedOrReadOnly]
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    status1 = models.CharField(max_length=255, null=True, blank=True)
    status2 = models.CharField(max_length=255, null=True, blank=True)
    status3 = models.CharField(max_length=255, null=True, blank=True)
    sandbox = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.username

# These usernames will not be run on the real social media platform
class WhatsappSandboxUserNames(BaseModel):
    whatsapp_username = models.ForeignKey(WhatsappUserNames, on_delete=models.CASCADE)

    def __str__(self):
        return self.whatsapp_username.username

# Model to track historical usernames for leads
class WhatsappLeadUserNames(BaseModel):
    whatsapp_username = models.ForeignKey(WhatsappUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track current username for leads
class WhatsappLead(BaseModel):
    whatsapp_username = models.ForeignKey(WhatsappLeadUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track historical usernames for sales representatives
class WhatsappSalesRepUserNames(BaseModel):
    whatsapp_username = models.ForeignKey(WhatsappUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

# Model to track current username for sales representatives
class WhatsappSalesRep(BaseModel):
    whatsapp_username = models.ForeignKey(WhatsappSalesRepUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

"""

Sales_Rep
    |
    |------WhatsappSalesrep
    |                |
    |                \|/
    |------WhatsappLeadUserNames

# same for lead
"""
