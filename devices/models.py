"""
Devices models module
"""
from django.db import models


class Device(models.Model):
    """
    Device model
    """

    serial_number = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)


class RecordingType(models.Model):
    """
    Recording Type
    """

    def __str__(self):
        return f'RecordingType ({self.id})'
