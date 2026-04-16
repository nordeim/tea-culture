"""
URL configuration for chayuan project.
"""

from django.contrib import admin
from django.urls import path

# Lazy import to allow Django apps to be ready first
from apps.api import api

# Initialize API if not already done
if api is None:
    from apps.api import init_api

    api = init_api()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
