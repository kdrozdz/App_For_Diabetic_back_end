from rest_framework.exceptions import ErrorDetail
from  rest_framework.test import APITestCase
from rest_framework import status
from Api.tests.data import account_data_patient


class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.data = account_data_patient

    def test_registration(self):
        response = self.client.post("/accounts/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_email_in_db(self):
        response = self.client.post("/accounts/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/accounts/", self.data)
        self.assertEqual(response.data, 'This email address is already being used')

    def test_registration_not_full_data(self):
        data = self.data
        data['email'] = False
        response = self.client.post("/accounts/", self.data)
        self.assertEqual(response.data, {'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]})
