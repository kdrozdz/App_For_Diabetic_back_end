from rest_framework import status
from rest_framework.test import APITestCase
from Api.models import Food
from Api.tests.data import Init
from accounts.models import Account
from rest_framework.authtoken.models import Token



class TestFoodCreate(APITestCase):
    url = '/food/'
    data = Init()

    def setUp(self):
        self.patient = Account.objects.create_user(**self.data.account_data_patient)
        self.token = Token.objects.create(user=self.patient)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_food(self):
        response = self.client.post(self.url, {'patient': self.patient.id,
                                               'name': 'Test',
                                               'carbs': 60,
                                               })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, 'Added')
        response2 = self.client.post(self.url, {'patient': self.patient.id,
                                               'name': 'Test',
                                               'carbs': 60,
                                               })
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data, 'You already have item with this name !')
