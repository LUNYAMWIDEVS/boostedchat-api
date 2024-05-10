from .helpers import helpers
from .helpers_circular import helpers_circular
from django.db.models import Q
from rest_framework import serializers
from django.utils import timezone
from django.db import models, IntegrityError, transaction

class ChannelManager:
    def __init__(self, channel):
        self.ChannelUserNames = helpers_circular.getChannelUserNameModel(channel)
        pass
    @transaction.atomic
    def save_channel_username(self, params = {}):
        """
        Saves a channel username. Updates or creates based on username and handles soft deletion.

        Args:
            params (dict, optional): A dictionary containing username and status information.
                Defaults to {}.
        """
        _, username, status1, status2, status3, sandbox, _ = helpers.getChannelUserNameParams(params)
        
        recordExists = self.ChannelUserNames.objects.filter(username=username ).exists()
        record_is_deleted = self.ChannelUserNames.objects.all_with_deleted().filter(username=username).exists()
        if record_is_deleted:
            self.ChannelUserNames.objects.all_with_deleted().filter(username=username).first().undelete()
        try:
            channel_username, created = self.ChannelUserNames.objects.get_or_create(
                username=username,
                defaults={
                    "status1": status1,
                    "status2": status2,
                    "status3": status3,
                    "sandbox": sandbox,
                },
            )

            # Update existing record if not created
            if not created:
                channel_username.status1 = status1
                channel_username.status2 = status2
                channel_username.status3 = status3
                channel_username.sandbox = sandbox

            channel_username.save() 
        except IntegrityError as e:
                if recordExists:
                    raise serializers.ValidationError(f"Username {username} already exists.")
                else:
                    raise serializers.ValidationError(f"Unknown erorr for {username}")

        return channel_username

    
    def read_channel_usernames(self, params = {}):
        """
        Reads usernames based on the provided parameters. Filters based on any non-None parameter present in the ChannelUserNames model.

        Args:
            params (dict, optional): A dictionary containing optional filter parameters.
                Defaults to {}.

        Returns:
            QuerySet: A queryset of ChannelUserNames objects filtered based on the params.
        """
        filters = Q()
        model_fields = {field.name for field in self.ChannelUserNames._meta.get_fields()}  # Get model field names
        for field, value in params.items():
            if value is not None and field in model_fields:  # Check for non-None value and valid field
                filters &= Q(**{field: value})
        return self.ChannelUserNames.objects.filter(filters)
    
    def read_channel_username(self, username):
        try:
            return self.ChannelUserNames.objects.get(username=username)
        except self.ChannelUserNames.DoesNotExist:
            return None

    def update_channel_username(self, params = {}):
        _, username, status1, status2, status3, sandbox, filters = helpers.getChannelUserNameParams(params, action="update")
        print(filters)
        channel_usernames = self.read_channel_usernames(filters) # user filters here
        for channel_username in channel_usernames:
            if channel_username:
                model_fields = {field.name for field in self.ChannelUserNames._meta.get_fields()}  # Get model field names
                for field, value in params.items():
                    if value is not None and field in model_fields:  # Check for non-None value and valid field
                        setattr(channel_username, field, value)
                channel_username.save()
                return True
        return False

    def delete_channel_username(self, username):
        channel_username = self.read_channel_username(username)
        if channel_username:
            channel_username.delete()
            return True
        return False

    def save_channel_lead_username(self, username, lead_id):
        instagram_lead_username = ChannelLeadUserNames(channel_username=self.read_channel_username(username), lead_id=lead_id)
        instagram_lead_username.save()

    def read_channel_lead_username(self, username):
        try:
            return ChannelLeadUserNames.objects.get(channel_username__username=username)
        except ChannelLeadUserNames.DoesNotExist:
            return None

    def update_channel_lead_username(self, username, new_lead_id):
        instagram_lead_username = self.read_channel_lead_username(username)
        if instagram_lead_username:
            instagram_lead_username.lead_id = new_lead_id
            instagram_lead_username.save()
            return True
        return False

    def delete_channel_lead_username(self, username):
        instagram_lead_username = self.read_channel_lead_username(username)
        if instagram_lead_username:
            instagram_lead_username.delete()
            return True
        return False

    def save_channel_lead(self, username, lead_id):
        instagram_lead = ChannelLead(channel_username=self.read_channel_lead_username(username), lead_id=lead_id)
        instagram_lead.save()

    def read_channel_lead(self, username):
        try:
            return ChannelLead.objects.get(channel_username__channel_username__username=username)
        except ChannelLead.DoesNotExist:
            return None

    def update_channel_lead(self, username, new_lead_id):
        instagram_lead = self.read_channel_lead(username)
        if instagram_lead:
            instagram_lead.lead_id = new_lead_id
            instagram_lead.save()
            return True
        return False

    def delete_channel_lead(self, username):
        instagram_lead = self.read_channel_lead(username)
        if instagram_lead:
            instagram_lead.delete()
            return True
        return False

    def save_channel_sales_rep_username(self, username, sales_rep_id):
        instagram_sales_rep_username = ChannelSalesRepUserNames(channel_username=self.read_channel_username(username), sales_rep_id=sales_rep_id)
        instagram_sales_rep_username.save()

    def read_channel_sales_rep_username(self, username):
        try:
            return ChannelSalesRepUserNames.objects.get(channel_username__username=username)
        except ChannelSalesRepUserNames.DoesNotExist:
            return None

    def update_channel_sales_rep_username(self, username, new_sales_rep_id):
        instagram_sales_rep_username = self.read_channel_sales_rep_username(username)
        if instagram_sales_rep_username:
            instagram_sales_rep_username.sales_rep_id = new_sales_rep_id
            instagram_sales_rep_username.save()
            return True
        return False

    def delete_channel_sales_rep_username(self, username):
        instagram_sales_rep_username = self.read_channel_sales_rep_username(username)
        if instagram_sales_rep_username:
            instagram_sales_rep_username.delete()
            return True
        return False

    def save_channel_sales_rep(self, username, sales_rep_id):
        instagram_sales_rep = ChannelSalesRep(channel_username=self.read_channel_sales_rep_username(username), sales_rep_id=sales_rep_id)
        instagram_sales_rep.save()

    def read_channel_sales_rep(self, username):
        try:
            return ChannelSalesRep.objects.get(channel_username__channel_username__username=username)
        except ChannelSalesRep.DoesNotExist:
            return None

    def update_channel_sales_rep(self, username, new_sales_rep_id):
        instagram_sales_rep = self.read_channel_sales_rep(username)
        if instagram_sales_rep:
            instagram_sales_rep.sales_rep_id = new_sales_rep_id
            instagram_sales_rep.save()
            return True
        return False

    def delete_channel_sales_rep(self, username):
        instagram_sales_rep = self.read_channel_sales_rep(username)
        if instagram_sales_rep:
            instagram_sales_rep.delete()
            return True
        return False