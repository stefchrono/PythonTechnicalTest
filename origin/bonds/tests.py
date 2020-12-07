import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from bonds.models import Bond
from bonds.serializers import BondSerializer


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username": "test_user", "password": "best_passname"}
        response = self.client.post('/register_api/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserViewSetTestCase(APITestCase):

    bonds_url = reverse("bonds")

    def setUp(self):
        self.user = User.objects.create_user(username="origin", password="markets")
        self.token = Token.objects.get(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_list_authenticated(self):
        response = self.client.get(self.bonds_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_list_non_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.bonds_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bonds_get_method(self):
        data = {"isin": "XXXXXX", "size": 1000000, 
                "currency": "USD", "maturity": 
                "2025-09-25", "lei": "7LTWFZYICNSX8D621K86", 
                "legal_name": ""}
        response = self.client.post('/bonds/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        