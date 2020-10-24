from Api.models import Patient, Doctor
from rest_framework.test import APITestCase
from Api.tests.data import Init

class CreateProfileTestCase(APITestCase):

    data = Init()

    def test_patient(self):
        self.client.post("/accounts/", self.data.account_data_patient)
        self.assertEqual(len(Patient.objects.all()), 1)

    def test_doctor(self):

        self.client.post("/accounts/", self.data.account_data_doctor)
        self.assertEqual(len(Doctor.objects.all()), 1)
