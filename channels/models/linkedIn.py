from django.db import models
from base.models import BaseModel
from sales_rep.models import SalesRep
from leads.models import Leads
from. import helpers
from django.db.models import Q

# Model to track LinkedIn usernames and their status
class LinkedInUserNames(BaseModel):
    autoLoad = True
   
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    status1 = models.CharField(max_length=255, null=True, blank=True)
    status2 = models.CharField(max_length=255, null=True, blank=True)
    status3 = models.CharField(max_length=255, null=True, blank=True)
    sandbox = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.username

# These usernames will not be run on the real social media platform
class LinkedInSandboxUserNames(BaseModel):
    linkedin_username = models.ForeignKey(LinkedInUserNames, on_delete=models.CASCADE)

    def __str__(self):
        return self.linkedin_username.username

# Model to track historical usernames for leads
class LinkedInLeadUserNames(BaseModel):
    linkedin_username = models.ForeignKey(LinkedInUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track current username for leads
class LinkedInLead(BaseModel):
    linkedin_username = models.ForeignKey(LinkedInLeadUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track historical usernames for sales representatives
class LinkedInSalesRepUserNames(BaseModel):
    linkedin_username = models.ForeignKey(LinkedInUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

# Model to track current username for sales representatives
class LinkedInSalesRep(BaseModel):
    linkedin_username = models.ForeignKey(LinkedInSalesRepUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

"""

Sales_Rep
    |
    |------LinkedInSalesrep
    |                |
    |                \|/
    |------LinkedInLeadUserNames

# same for lead
"""

