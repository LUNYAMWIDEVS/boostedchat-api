from django.db import models

from authentication.models import User
from base.models import BaseModel
from instagram.models import Account
from setup.utils import setuputils
from setup.utils import modelManager


# Create your models here.
class SalesRep(BaseModel):
    # class Meta:
    #     # Define meta options
    autoLoad = True
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    ig_username = models.CharField(max_length=255, null=True, blank=True)
    ig_password = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.ManyToManyField(Account, blank=True)
    available = models.BooleanField(default=True)
    country = models.TextField(default="US")
    city = models.TextField(default="Pasadena")

    def __str__(self) -> str:
        return self.user.email

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
