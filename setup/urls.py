"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from setup.utils.app_api_generator import router
# from .app_api_generator import router
from .app_api_generator import APIRouterGenerator
router = APIRouterGenerator().router

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "BoostedChat Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api-auth/", include("rest_framework.urls")),  # new
    path("v1/authentication/", include("authentication.urls")),
    path("v1/instagram/", include("instagram.urls")),
    path("v1/sales/", include("sales_rep.urls")),
    path("v1/leads/", include("leads.urls")),
    path("v1/logs/", include("audittrails.urls")),
    path("v1/dialogflow/", include("dialogflow.urls")),
    # path('v1/outreaches/', include('outreaches.urls')),
    # path('v1/channels/', include('channels.urls')),  # Include app-specific URLs
    path('v1/', include(router.urls)), # Ref: https://gist.github.com/D2theR/0b439164e94a9577d4b502496c7672cf

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
