from accounts.models import Account
from django.db import models


class Sugar_level(models.Model):
    level = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    without_a_meal = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE , related_name='sugar_level')


class Patient(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, null=True, related_name='patient')

    def __str__(self):
        return f'{self.account.email} {self.account}'


class Doctor(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.account.email} {self.account} '


class Cooperate(models.Model):
    sender = models.ForeignKey(Account, related_name='user_sender_cooperate', on_delete=models.DO_NOTHING)
    reciver = models.ForeignKey(Account, related_name='user_reciver_cooperate', on_delete=models.DO_NOTHING)
    accept_sender = models.BooleanField(default=False)
    accept_reciver = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)


class Chat(models.Model):
    sender = models.ForeignKey(Account, related_name='user_sender_email', on_delete=models.DO_NOTHING)
    reciver = models.ForeignKey(Account, related_name='user_reciver_email', on_delete=models.DO_NOTHING)
    is_new = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()
