
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from bonds.models import Bond
from bonds.serializers import BondSerializer


class UserCreateTestCase(APITestCase):
    def test_registration(self):
        data = {"username": "test_user", "password": "best_passname"}
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class HelloWorldTestCase(APITestCase):

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

    def test_bonds_post_method(self):
        data = {"isin": "XXXXXX", 
                "size": 1000000, 
                "currency": "USD", 
                "maturity": "2025-09-25", 
                "lei": "R0MUWSFPU8MPRO8K5P83", 
                "legal_name": ""}
        response = self.client.post('/bonds/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['legal_name'], "BNP PARIBAS")
        

    def test_bonds_get_method(self):
        response = self.client.get('/bonds/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_filter(self):
        response = self.client.get('/bonds/?legal_name=BNP PARIBAS')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ModelsTestCase(TestCase):
    def setUp(self):
        Bond.objects.create(isin="FR0000131104", 
                            size="10000000",
                            currency="EUR", 
                            maturity="2025-02-28", 
                            lei="R0MUWSFPU8MPRO8K5P83", 
                            legal_name="")
        
        Bond.objects.create(isin="GR123456789", 
                            size="10000000",
                            currency="EUR", 
                            maturity="2025-02-28", 
                            lei="FAKE", 
                            legal_name="")

    def test_legal_name(self):
        test_actual_bond = Bond.objects.get(isin="FR0000131104")
        test_fake_bond = Bond.objects.get(isin="GR123456789")
        self.assertEqual(str(test_actual_bond.legal_name), "BNP PARIBAS")
        self.assertEqual(str(test_fake_bond.legal_name), "Unknown Legal Name")

