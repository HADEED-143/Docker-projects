"""
URL configuration for LaborWorld project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# for file handling
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Labor World API",
        default_version='v1',
        description="Labor world API for job seekers and employers",
        terms_of_service="",
        contact=openapi.Contact(email="zulabdin21@gmail.com"),
        license=openapi.License(name="Riphah License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path('auth/', include('djoser.urls')),     # for djoser
    path('auth/', include('djoser.urls.authtoken')),      # for djoser
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),     # for swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),      # for redoc

    path('api/', include('profile_management.urls')),
    path('api/', include('Jobs.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('chat.urls')),

]


# for file handlings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
