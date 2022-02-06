from rest_framework import serializers
from .models import GlucoseLevel


default_glucose_level_fields = [
    'id',
    'created_by',
    'device',
    'device_timestamp',
    'recording_type',
    'glucose_value_history',
    'glucose_scan',
]


class GlucoseLevelListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.name')

    class Meta:
        model = GlucoseLevel
        fields = default_glucose_level_fields


class GlucoseLevelSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.name')

    class Meta:
        model = GlucoseLevel
        fields = default_glucose_level_fields + [
            'rapid_acting_insulin',
            'rapid_acting_insulin_units',
            'nutritional_data',
            'carbohydrates_grams',
            'carbohydrates_servings',
            'depot_insulin',
            'depot_insulin_units',
            'notes',
            'glucose_test_strips',
            'ketone',
            'meal_insulin',
            'correction_insulin',
            'user_insulin_changes',
        ]
