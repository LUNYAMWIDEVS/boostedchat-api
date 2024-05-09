from django.db import models
from base.models import BaseModel
from sales_rep.models import SalesRep
from leads.models import Leads
from. import helpers
from django.db.models import Q

# Model to track Sandbox usernames and their status
class SandboxUserNames(BaseModel):
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    status1 = models.CharField(max_length=255, null=True, blank=True)
    status2 = models.CharField(max_length=255, null=True, blank=True)
    status3 = models.CharField(max_length=255, null=True, blank=True)
    sandbox = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.username

# These usernames will not be run on the real social media platform
class SandboxSandboxUserNames(BaseModel):
    sandbox_username = models.ForeignKey(SandboxUserNames, on_delete=models.CASCADE)

    def __str__(self):
        return self.sandbox_username.username

# Model to track historical usernames for leads
class SandboxLeadUserNames(BaseModel):
    sandbox_username = models.ForeignKey(SandboxUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track current username for leads
class SandboxLead(BaseModel):
    sandbox_username = models.ForeignKey(SandboxLeadUserNames, on_delete=models.CASCADE)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

# Model to track historical usernames for sales representatives
class SandboxSalesRepUserNames(BaseModel):
    sandbox_username = models.ForeignKey(SandboxUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

# Model to track current username for sales representatives
class SandboxSalesRep(BaseModel):
    sandbox_username = models.ForeignKey(SandboxSalesRepUserNames, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(SalesRep, on_delete=models.CASCADE)

"""

Sales_Rep
    |
    |------SandboxSalesrep
    |                |
    |                \|/
    |------SandboxLeadUserNames

# same for lead
"""

