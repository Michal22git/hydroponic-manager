from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..models import HydroponicSystem, Measurement


class HydroponicSystemViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_system(self):
        url = reverse('hydroponic-system-list')
        data = {
            'name': 'Test System',
            'description': 'Test Description'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 1)
        self.assertEqual(HydroponicSystem.objects.get().name, 'Test System')
        
    def test_list_systems(self):
        HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System 1'
        )
        HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System 2'
        )
        
        url = reverse('hydroponic-system-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)


class MeasurementViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(
            owner=self.user,
            name='Test System'
        )
        
    def test_create_measurement(self):
        url = reverse('measurement-list')
        data = {
            'system': self.system.id,
            'ph': 7.0,
            'tds': 500,
            'water_temperature': 25.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Measurement.objects.count(), 1)
        
    def test_filter_measurements(self):
        Measurement.objects.create(
            system=self.system,
            ph=6.5,
            tds=450,
            water_temperature=24.0
        )
        Measurement.objects.create(
            system=self.system,
            ph=7.5,
            tds=550,
            water_temperature=26.0
        )
        
        url = reverse('measurement-list')
        response = self.client.get(f'{url}?ph_min=7.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_measurement(self):
        measurement = Measurement.objects.create(
            system=self.system,
            ph=7.0,
            tds=500,
            water_temperature=25.0
        )
        url = reverse('measurement-detail', args=[measurement.id])
        data = {'ph': 7.5}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        measurement.refresh_from_db()
        self.assertEqual(measurement.ph, 7.5) 

    def test_delete_measurement(self):
        measurement = Measurement.objects.create(
            system=self.system,
            ph=7.0,
            tds=500,
            water_temperature=25.0
        )   
        url = reverse('measurement-detail', args=[measurement.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Measurement.objects.count(), 0)

    def test_get_measurement_details(self):
        measurement = Measurement.objects.create(
            system=self.system,
            ph=7.0,
            tds=500,
            water_temperature=25.0)
        url = reverse('measurement-detail', args=[measurement.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ph'], 7.0)
        self.assertEqual(response.data['tds'], 500)
        self.assertEqual(response.data['water_temperature'], 25.0)
