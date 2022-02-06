"""
Devices app admin file
"""

from django.contrib import admin

from devices.models import Device, RecordingType


class DeviceAdmin(admin.ModelAdmin):
    """
    Device admin class
    """

    model = Device


class RecordingTypeAdmin(admin.ModelAdmin):
    """
    Recording Type admin class
    """

    model = RecordingType


admin.site.register(Device, DeviceAdmin)
admin.site.register(RecordingType, RecordingTypeAdmin)
