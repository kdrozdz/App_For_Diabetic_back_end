from rest_framework import status
from rest_framework.test import APITestCase
from Api.models import SugarLevel
from Api.tests.data import Init
from accounts.models import Account
from rest_framework.authtoken.models import Token


class TestSugarViews(APITestCase):
    url_sugar = '/sugar/'
    data = Init()

    def setUp(self):
        self.account = Account.objects.create_user(**self.data.account_data_patient)
        self.token = Token.objects.create(user=self.account)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_sugar(self):
        for _ in range(3):
            response = self.client.post(self.url_sugar, {**self.data.sugar_data})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(SugarLevel.objects.all()), 3)

    def test_all_info(self):
        for index, _ in enumerate(range(6)):
            self.data.sugar_data['level'] += index * 10
            self.data.sugar_data['without_a_meal'] = False if index % 3 == 0 else True
            response = self.client.post(self.url_sugar, {**self.data.sugar_data})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/sugar/all_info/', {'pk': self.account.id})
        self.assertEqual(response.data['avreage_all_fast_blood_sugar'],  173)
        self.assertEqual(response.data['avreage_all_sugars'], 158)
        self.assertEqual(response.data['avreage_last_five_sugars'], 170)
        self.assertEqual(len(response.data['list_of_all_sugars']), 6)

    def test_all_info_null_data_new_users(self):
        response = self.client.post('/sugar/all_info/', {'pk': self.account.id})
        self.assertEqual(response.data['avreage_all_fast_blood_sugar'], 0)
        self.assertEqual(response.data['avreage_all_sugars'], 0)
        self.assertEqual(response.data['avreage_last_five_sugars'], 0)
        self.assertEqual(len(response.data['list_of_all_sugars']), 0)
