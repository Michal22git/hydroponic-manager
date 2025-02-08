from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import HydroponicSystem, Measurement


class HydroponicSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_create_system(self):
        system = HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System',
            description='Test Description'
        )
        self.assertEqual(system.name, 'Test System')
        self.assertEqual(system.owner, self.user)
        
    def test_system_str_representation(self):
        system = HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System'
        )
        self.assertEqual(str(system), 'Test System')
        self.assertEqual(system.name, 'Test System')
        self.assertTrue(isinstance(str(system), str))


class MeasurementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.system = HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System'
        )
        
    def test_create_measurement(self):
        measurement = Measurement.objects.create(
            system=self.system,
            ph=7.0,
            tds=500,
            water_temperature=25.0
        )
        self.assertEqual(measurement.ph, 7.0)
        self.assertEqual(measurement.system, self.system)
        
    def test_ph_validation(self):
        with self.assertRaises(ValidationError):
            measurement = Measurement(
                system=self.system,
                ph=15.0,
                tds=500,
                water_temperature=25.0
            )
            measurement.full_clean()

    def test_measurement_str_representation(self):
        measurement = Measurement.objects.create(
            system=self.system,
            ph=7.0,
            tds=500,
            water_temperature=25.0
        )
        expected_str = "System: Test System | pH: 7.0 | TDS: 500 | Temp: 25.0°C"
        self.assertEqual(str(measurement), expected_str) 