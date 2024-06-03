from django.db import models
from setup.utils import modelManager
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from base.models import BaseModel


class Channel(models.Model):
    name = models.CharField(max_length=100, unique=True, ) # case insensitive
    docker_url = models.CharField(max_length=255, blank=False)
    external_url = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)


    autoLoad = True
    permissionClasses = [IsAuthenticatedOrReadOnly]
    modelManager = modelManager

    def __str__(self) -> str:
        return self.name
    
class ChannelActivity(models.Model):
    autoLoad = True
    permissionClasses = [IsAuthenticated]
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255) # defined any activity that can be done on this channel
    description = models.TextField(blank=True, null=True)
    class Meta:
        unique_together = ('channel', 'activity')

    def __str__(self):
        return self.channel.name + " - " + self.activity
