from accounts.models import Account
from django.db import models


class SugarLevel(models.Model):
    level = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    without_a_meal = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sugar_level')


class Patient(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, null=True, blank=True, related_name='patient')

    def __str__(self):
        return f'{self.account.email} {self.account}'


class Doctor(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='doctor')

    def __str__(self):
        return f' {self.account.email} {self.account} '


class Cooperate(models.Model):
    patient = models.ForeignKey(Account, related_name='patient_cooperate', on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(Account, related_name='doctor_cooperate', on_delete=models.DO_NOTHING)
    accept_patient = models.BooleanField(default=False)
    accept_doctor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    how_rejected = models.ForeignKey(Account, related_name='how_rejected', on_delete=models.DO_NOTHING, null=True, blank=True)
    rejected = models.BooleanField(default=False)
    message = models.TextField(max_length=256, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class RejectCooperate(models.Model):
    how_rejected = models.ForeignKey(Account, related_name='reject_cooperate', on_delete=models.DO_NOTHING)
    send_info_to = models.ForeignKey(Account, related_name='send_to', on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    message = models.TextField()

class Chat(models.Model):
    sender = models.ForeignKey(Account, related_name='sender', on_delete=models.DO_NOTHING)
    doctorId = models.ForeignKey(Account, related_name='user_sender_email', on_delete=models.DO_NOTHING)
    patientId = models.ForeignKey(Account, related_name='user_reciver_email', on_delete=models.DO_NOTHING)
    is_new = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class Advice(models.Model):
    patient = models.ForeignKey(Account, related_name='patient_advice', on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(Account, related_name='doctor_advice', on_delete=models.DO_NOTHING)
    message = models.TextField(max_length=512)
    is_new = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)




