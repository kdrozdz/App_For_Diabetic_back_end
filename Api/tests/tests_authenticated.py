from accounts.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from Api.tests.data import Init


class TestAuthenticatedViews(APITestCase):

    url_accounts = '/accounts/'
    url_patient = '/patient/'
    url_doctors = '/doctors/'

    def setUp(self):
        self.data = Init()
        self.account = Account.objects.create_user(**self.data.account_data_patient)
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
