from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import GenericViewSet

from .filters import GlucoseLevelFilterSet
from .models import GlucoseLevel
from .pagination import StandardResultsSetPagination
from .serializers import (
    GlucoseLevelSerializer,
    GlucoseLevelListSerializer,
    default_glucose_level_fields,
)


class GlucoseLevelViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = GlucoseLevelSerializer
    queryset = GlucoseLevel.objects.all().select_related('created_by')
    filterset_class = GlucoseLevelFilterSet
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    pagination_class = StandardResultsSetPagination
    ordering_fields = default_glucose_level_fields

    def get_serializer_class(self):
        if self.action == 'list':
            return GlucoseLevelListSerializer
        return GlucoseLevelSerializer


class LevelsListView(TemplateView):
    template_name = 'levels_list.html'
