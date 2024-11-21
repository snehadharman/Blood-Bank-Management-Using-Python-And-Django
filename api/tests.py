from django.test import TestCase

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Donor, BloodInventory, BloodRequest

class TestSetup(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="user123"
        )
        self.client = APIClient()


def test_blood_request_requires_authentication(self):
    response = self.client.get('/api/blood-requests/')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def test_create_blood_request(self):
    self.client.force_authenticate(user=self.user)
    data = {'blood_type': 'O+', 'units_requested': 2, 'reason': 'Surgery'}
    response = self.client.post('/api/blood-requests/', data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(BloodRequest.objects.count(), 1)
    self.assertEqual(BloodRequest.objects.first().user, self.user)


def test_admin_can_view_all_requests(self):
    BloodRequest.objects.create(
        blood_type='A-', units_requested=3, reason='Accident', user=self.user
    )
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.get('/api/blood-requests/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

def test_user_can_view_only_their_requests(self):
    BloodRequest.objects.create(
        blood_type='A-', units_requested=3, reason='Accident', user=self.user
    )
    another_user = User.objects.create_user(
        username="another", email="another@example.com", password="another123"
    )
    BloodRequest.objects.create(
        blood_type='B+', units_requested=2, reason='Donation', user=another_user
    )
    self.client.force_authenticate(user=self.user)
    response = self.client.get('/api/blood-requests/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)  # Only the first request is visible



