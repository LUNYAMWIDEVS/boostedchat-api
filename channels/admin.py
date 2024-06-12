from django.contrib import admin
from .models import Channel, ChannelActivity
# Register your models here.
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

# register ChannelActivities
@admin.register(ChannelActivity)
class ChannelActivitiesAdmin(admin.ModelAdmin):
    # search_fields = ['channel', 'activity']
    pass