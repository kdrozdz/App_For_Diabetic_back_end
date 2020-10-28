from rest_framework import status
from rest_framework.test import APITestCase
from Api.models import SugarLevel
from Api.tests.data import Init
from accounts.models import Account
from rest_framework.authtoken.models import Token



class TestCooperateViews(APITestCase):
    url_cooperate = '/cooperate/'
    url_have_i_sent = 'have_i_sent_cooperate/'
    url_rejected= 'reject_cooperate/'
    data = Init()

    def setUp(self):
        self.patient = Account.objects.create_user(**self.data.account_data_patient)
        self.doctor = Account.objects.create_user(**self.data.account_data_doctor)
        self.token = Token.objects.create(user=self.patient)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_cooperate(self):
        response = self.client.post(self.url_cooperate, {'patient':self.patient.id, 'doctor': self.doctor.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient'], 1)
        self.assertEqual(response.data['doctor'], 2)


    def test_i_have_sent_cooperate(self):
        first_response = self.client.post(self.url_cooperate + self.url_have_i_sent, {'pk': self.patient.id})
        self.assertEqual(first_response.data, {'go_to_doctor_list': True})
        self.client.post(self.url_cooperate, {'patient': self.patient.id, 'doctor': self.doctor.id})
        second_response = self.client.post(self.url_cooperate + self.url_have_i_sent , {'pk': self.patient.id})
        self.assertEqual(second_response.data['go_to_doctor_list'], False )

    def test_rejected_cooperate(self):
        self.client.post(self.url_cooperate, {'patient': self.patient.id, 'doctor': self.doctor.id})
        first_response = self.client.post(self.url_cooperate + self.url_have_i_sent, {'pk': self.patient.id})
        self.assertEqual(first_response.data['go_to_doctor_list'], False)
        self.client.post(self.url_cooperate + self.url_rejected, {'pk': first_response.data['id']})
        second_response = self.client.post(self.url_cooperate + self.url_have_i_sent, {'pk': self.patient.id})
        self.assertEqual(second_response.data, {'go_to_doctor_list': True})