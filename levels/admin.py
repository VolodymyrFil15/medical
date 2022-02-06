from django.contrib import admin

from levels.models import GlucoseLevel


class GlucoseLevelAdmin(admin.ModelAdmin):
    model = GlucoseLevel


admin.site.register(GlucoseLevel, GlucoseLevelAdmin)
