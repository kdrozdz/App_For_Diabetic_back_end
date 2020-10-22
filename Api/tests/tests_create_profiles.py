from Api.models import Patient, Doctor
from rest_framework.test import APITestCase
from Api.tests.data import account_data

class CreateProfileTestCase(APITestCase):

    def setUp(self):

        self.data = {
            'password': 'test123',
            'last_name': 'test123',
            'first_name': 'test123',
            'email': 'test123@test.com',
            'age': 32,
            'profile': 0,
            'phone_number': 999888444,
        }

    def test_patient(self):
        self.client.post("/accounts/", self.data)
        self.assertEqual(len(Patient.objects.all()), 1)

    def test_doctor(self):
        self.data['profile'] = 1
        self.client.post("/accounts/", self.data)
        self.assertEqual(len(Doctor.objects.all()), 1)
