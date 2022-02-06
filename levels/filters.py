from django_filters import rest_framework as filters

from .models import GlucoseLevel


class GlucoseLevelFilterSet(filters.FilterSet):
    class Meta:
        model = GlucoseLevel
        fields = ('user_id', 'start', 'stop')

    user_id = filters.CharFilter(field_name='created_by__name')
    start = filters.DateTimeFilter(
        field_name='device_timestamp',
        lookup_expr='gte',
    )
    stop = filters.DateTimeFilter(
        field_name='device_timestamp',
        lookup_expr='lte',
    )
