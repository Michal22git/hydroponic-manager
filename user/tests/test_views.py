from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserRegisterTests(APITestCase):
    def test_create_user(self):
        url = reverse('user_register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_create_user_with_short_password(self):
        url = reverse('user_register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test',
            'password2': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        
    def test_login_user(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data) 