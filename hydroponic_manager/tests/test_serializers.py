from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from ..models import HydroponicSystem, Measurement
from ..serializers import (
    HydroponicSystemSerializer,
    MeasurementCreateSerializer
)


class HydroponicSystemSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.system = HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System',
            description='Test Description'
        )
        
    def test_contains_expected_fields(self):
        serializer = HydroponicSystemSerializer(instance=self.system)
        data = serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'name', 'description', 'created_at', 'updated_at', 
             'owner', 'latest_measurements', 'measurement_count']
        )


class MeasurementSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.system = HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System'
        )
        self.measurement = Measurement.objects.create(
            system=self.system,
            ph=7.0,
            tds=500,
            water_temperature=25.0
        )
        
    def test_measurement_serializer_validation(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.user
        
        data = {
            'system': self.system.id,
            'ph': 7.0,
            'tds': 500,
            'water_temperature': 25.0
        }
        
        serializer = MeasurementCreateSerializer(
            data=data,
            context={'request': request}
        )
        self.assertTrue(serializer.is_valid()) 