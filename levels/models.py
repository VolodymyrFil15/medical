from django.db import models

from devices.models import Device, RecordingType


class User(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'User ({self.name})'


class GlucoseLevel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(
        Device, on_delete=models.SET_NULL, null=True, verbose_name='Device'
    )
    device_timestamp = models.DateTimeField()

    recording_type = models.ForeignKey(
        RecordingType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Revording type',
    )

    glucose_value_history = models.IntegerField(
        'Glucose value history mg/dL',
        null=True,
    )
    glucose_scan = models.IntegerField(
        'Glucose scan mg/dL',
        null=True,
    )

    rapid_acting_insulin = models.CharField(
        'Non-numeric rapid-acting insulin',
        null=True,
        max_length=128,
    )
    rapid_acting_insulin_units = models.IntegerField(
        'Rapid-Acting Insulin (Units)',
        null=True,
    )

    nutritional_data = models.CharField(
        'Non-numeric nutritional data',
        null=True,
        max_length=128,
    )
    carbohydrates_grams = models.IntegerField(
        'Carbohydrates (grams)',
        null=True,
    )
    carbohydrates_servings = models.IntegerField(
        'Carbohydrates (servings)',
        null=True,
    )

    depot_insulin = models.CharField(
        'Non-numeric depot insulin',
        null=True,
        max_length=128,
    )
    depot_insulin_units = models.IntegerField(
        'Depot insulin (units)',
        null=True,
    )

    notes = models.TextField(null=True)

    glucose_test_strips = models.IntegerField(
        'Glucose test strips mg/dL',
        null=True,
    )
    ketone = models.IntegerField('Ketone mmol/L', null=True)

    meal_insulin = models.IntegerField('Meal Insulin (units)', null=True)
    correction_insulin = models.IntegerField(
        'Correction insulin (units)',
        null=True,
    )
    user_insulin_changes = models.IntegerField(
        'User Insulin Change (Units)',
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_item_for_user',
                fields=['created_by', 'device_timestamp'],
            )
        ]
        ordering = ['device_timestamp']
