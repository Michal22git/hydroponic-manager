from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import HydroponicSystem, Measurement
from .serializers import (
    HydroponicSystemSerializer,
    MeasurementSerializer,
    MeasurementCreateSerializer,
)


class MeasurementFilter(filters.FilterSet):
    """Filter for measurements allowing filtering by date ranges and values."""
    
    created_at_after = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text="Filter measurements taken after specified date",
    )
    created_at_before = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text="Filter measurements taken before specified date",
    )
    ph_min = filters.NumberFilter(
        field_name='ph',
        lookup_expr='gte',
        help_text="Minimum pH value",
    )
    ph_max = filters.NumberFilter(
        field_name='ph',
        lookup_expr='lte',
        help_text="Maximum pH value",
    )
    tds_min = filters.NumberFilter(
        field_name='tds',
        lookup_expr='gte',
        help_text="Minimum TDS value",
    )
    tds_max = filters.NumberFilter(
        field_name='tds',
        lookup_expr='lte',
        help_text="Maximum TDS value",
    )
    temperature_min = filters.NumberFilter(
        field_name='water_temperature',
        lookup_expr='gte',
        help_text="Minimum water temperature",
    )
    temperature_max = filters.NumberFilter(
        field_name='water_temperature',
        lookup_expr='lte',
        help_text="Maximum water temperature",
    )

    class Meta:
        model = Measurement
        fields = {
            'system': ['exact'],
            'ph': ['exact', 'lt', 'gt'],
            'tds': ['exact', 'lt', 'gt'],
            'water_temperature': ['exact', 'lt', 'gt'],
        }


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing hydroponic systems.
    
    Provides standard CRUD operations for hydroponic systems.
    Each user has access only to their own systems.
    """
    
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Returns queryset containing only systems belonging to the logged-in user."""
        return HydroponicSystem.objects.select_related('owner').filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):
        """Saves a new hydroponic system, setting the owner to the logged-in user."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Get system details with latest measurements."""
        system = self.get_object()
        serializer = self.get_serializer(system)
        return Response(serializer.data)


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing measurements.
    
    Allows adding and viewing measurements for hydroponic systems.
    Users can manage only measurements from their own systems.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = MeasurementFilter
    ordering_fields = ['created_at', 'ph', 'tds', 'water_temperature']
    ordering = ['-created_at']

    def get_queryset(self):
        """Returns queryset containing only measurements from systems belonging to the logged-in user."""
        return Measurement.objects.select_related('system', 'system__owner').filter(
            system__owner=self.request.user
        )

    def get_serializer_class(self):
        """
        Selects appropriate serializer based on the action.
        
        Uses MeasurementCreateSerializer for create and update operations,
        MeasurementSerializer for other operations.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return MeasurementCreateSerializer
        return MeasurementSerializer
