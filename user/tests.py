import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from django.test import Client
from .forms import LoginForm

class ProxyUserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('proxy-login')
        self.credentials = {
            'email': 'test@test.com',
            'phone': '8090000000',
            'password': 'password123'
        }

    @patch('requests.post')
    def test_proxy_user_success(self, mock_post):
        """Test successful login via the external API"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'token': 'dummy_token'
        }

        response = self.client.post(self.url, self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    @patch('requests.post')
    def test_proxy_user_failed(self, mock_post):
        """Test failed login via the external API"""
        mock_post.return_value.status_code = 401

        response = self.client.post(self.url, self.credentials, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'Failed to fetch Ciento API')

    @patch('requests.post')
    def test_proxy_user_exception(self, mock_post):
        """Test exception handling when calling external API"""
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        response = self.client.post(self.url, self.credentials, format='json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Network error')

class LoginViewTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    @patch('requests.get')
    @patch('requests.post')
    def test_login_view_success(self, mock_post, mock_get):
        """Test successful login and membership retrieval"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access': 'dummy_token',
            'refresh': 'dummy_refresh_token'
        }
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'results': 'Membership Data'}
        
        form_data = {
            'email': 'test@test.com',
            'phone': '1234567890',
            'password': 'password123'
        }

        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Membership Data', response.content.decode())

    @patch('requests.post')
    def test_login_view_invalid_credentials(self, mock_post):
        """Test login view with invalid credentials"""
        mock_post.return_value.status_code = 401
        
        form_data = {
            'email': 'invalid@test.com',
            'phone': '1234567890',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Login Failed', response.content.decode())

    def test_login_view_get_request(self):
        """Test rendering the login form on GET request"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

