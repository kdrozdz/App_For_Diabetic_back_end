from rest_framework import status
from rest_framework.test import APITestCase
from Api.tests.data import Init
from accounts.models import Account
from rest_framework.authtoken.models import Token


class TestCooperateViews(APITestCase):
    url_chat = '/chat/'

    data = Init()

    def setUp(self):
        self.patient = Account.objects.create_user(**self.data.account_data_patient)
        self.doctor = Account.objects.create_user(**self.data.account_data_doctor)
        self.token = Token.objects.create(user=self.patient)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_chat(self):
        response = self.client.post(self.url_chat, {'patientId': self.patient.id, 'doctorId': self.doctor.id,
                                                    'sender': self.patient.id, 'message': 'test'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {'id': 1, 'is_new': False, 'date': response.data['date'], 'message': 'test', 'sender': 1,
                          'doctorId': 2, 'patientId': 1})
