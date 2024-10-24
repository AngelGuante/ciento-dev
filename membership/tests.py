from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from .models import Membership

class ProxyMembershipTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('membership')
        self.token = 'validToken'

    @patch('requests.get')
    def test_proxy_membership_missing_auth(self, mock_get):
        """Test case when Authorization header is missing"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Authorization header not provided')

    @patch('requests.get')
    def test_proxy_membership_success(self, mock_get):
        """Test successful API call to external service"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'membership': 'details'}

        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'membership': 'details'})

        # Ensure the correct call was made to the external API
        mock_get.assert_called_once_with(
            'https://ciento-server-jk6skids3q-uc.a.run.app/membership',
            headers={'Authorization': f'Bearer {self.token}'}
        )

    @patch('requests.get')
    def test_proxy_membership_failed(self, mock_get):
        """Test failed API call to external service"""
        mock_get.return_value.status_code = 500

        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data['error'], 'Failed to fetch Ciento API')

class MembershipListCreateTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('membership_list_create')
        self.membershipData = {
            'email': 'mail@test.com',
            'full_name': 'test name',
            'phone_number': '8090000000'
        }

    def test_list_memberships(self):
        """Test listing memberships"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_membership(self):
        """Test creating a new membership"""
        response = self.client.post(self.url, self.membershipData, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Membership.objects.filter(email='mail@test.com').exists())

class MembershipDetailTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.membershipData = {
            'email': 'mail@test.com',
            'full_name': 'test name',
            'phone_number': '8090000000'
        }
        self.membership = Membership.objects.create(email=self.membershipData['email'], full_name=self.membershipData['full_name'], phone_number=self.membershipData['phone_number'])
        self.url = reverse('membership_detail', kwargs={'id': self.membership.id})

    def test_retrieve_membership(self):
        """Test retrieving a membership by ID"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.membership.email)
    
    def test_update_membership(self):
        """Test updating a membership"""
        data = {
            'email': 'mailUpdated@test.com',
            'full_name': 'test name',
            'phone_number': '8090000000'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'mailUpdated@test.com')

    def test_delete_membership(self):
        """Test deleting a membership"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Membership.objects.filter(id=self.membership.id).exists())

    def test_retrieve_nonexistent_membership(self):
        """Test retrieving a non-existent membership"""
        non_existent_url = reverse('membership_detail', kwargs={'id': 9999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_membership(self):
        """Test updating a non-existent membership"""
        non_existent_url = reverse('membership_detail', kwargs={'id': 9999})
        data = {
            'email': 'nonexistent@test.com',
            'full_name': 'Non-existent',
            'phone_number': '0000000000'
        }
        response = self.client.put(non_existent_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_membership(self):
        """Test deleting a non-existent membership"""
        non_existent_url = reverse('membership_detail', kwargs={'id': 9999})
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
