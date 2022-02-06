"""
Devices apps module
"""
from django.apps import AppConfig


class DevicesConfig(AppConfig):
    """
    Devices app config
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devices'
