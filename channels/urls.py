# from django.urls import path, include
# from rest_framework import routers
# from outreaches.views import PeriodicTaskViewSet, TasksViewSet, TaskViewSet

# from .views import ProtectedView
# router = routers.DefaultRouter()
# router.register(r'protected', ProtectedView, basename='protected-view')

# urlpatterns = [
#     path('', include(router.urls)),  # Include router URLs for the viewset
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'channels', ChannelsViewSet, basename='channels')
router.register(r'channelusernames', ChannelUserNameViewSet, basename='channelusernames')
router.register(r'instagram', InstagramViewSet, basename='instagram')


urlpatterns = [
    path('', include(router.urls)),
    # Other URL patterns
]
