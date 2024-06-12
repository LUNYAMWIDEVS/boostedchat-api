# from rest_framework.routers import DefaultRouter

# from .views import LeadManager

# router = DefaultRouter()
# router.register(r"", LeadManager, basename="leads")


# urlpatterns = router.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadManager, LeadsViewSet


router = DefaultRouter()
router.register(r"leads", LeadManager, basename="leads")
router.register(r'lead', LeadsViewSet, basename="lead")

urlpatterns = [
    path('', include(router.urls)),
]