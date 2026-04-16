"""
CHA YUAN API App Configuration
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration for the API app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.api"
    verbose_name = "API"

    def ready(self):
        """Register API routers when Django apps are ready."""
        # Import and register routers
        from apps.api import register_routers

        register_routers()
