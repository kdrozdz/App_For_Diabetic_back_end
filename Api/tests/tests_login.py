from rest_framework.exceptions import ErrorDetail
from accounts.models import Account
from rest_framework.test import APITestCase
from rest_framework import status
from Api.tests.data import Init


class TestAuthenticatedViews(APITestCase):

    url_auth = '/auth/'

    def setUp(self):
        self.data = Init()
        self.account = Account.objects.create_user(**self.data.account_data_patient)

    def test_login_return_token_id_profile(self):
        response = self.client.post(self.url_auth, {'username': self.account.email, 'password': self.data.account_data_patient['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'token': response.data['token'], 'id': 1, 'profile': 'Patient'})

    def test_login_invalid_credentials(self):
        response = self.client.post(self.url_auth, {'username': self.account.email, 'password': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [ErrorDetail(string='Unable to log in with provided credentials.', code='authorization')]})
