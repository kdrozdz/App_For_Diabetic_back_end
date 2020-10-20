from accounts.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class TestAuthenticatedViews(APITestCase):

    url_accounts = '/accounts/'
    url_patient = '/patient/'
    url_doctors = '/doctors/'


    def setUp(self):
        self.account = Account.objects.create_user(
            password='test123',
            last_name='test123',
            first_name='test123',
            email='test123@test.com',
            age=32,
            profile=0,
            phone_number=999888444,
        )
        self.token = Token.objects.create(user=self.account)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)


    def test_accounts_authenticated(self):
        response = self.client.get(self.url_accounts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accounts_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url_accounts)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_authenticated(self):
        response = self.client.get(self.url_accounts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url_accounts)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_doctors_authenticated(self):
        response = self.client.get(self.url_accounts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctors_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url_accounts)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
