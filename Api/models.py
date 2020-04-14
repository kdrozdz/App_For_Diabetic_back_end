from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save ,sender=User)
def create_auth_token(sender,instance=None , created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
        if instance.is_staff:
            Doctor.objects.create(user=instance)
        else:
            Patient.objects.create(user=instance)


class Sugar_level(models.Model):
    level = models.IntegerField()
    data = models.DateTimeField(auto_now=True)
    without_a_meal=models.BooleanField(default=False)
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE  ,related_name='sugar')


class Patient(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor',on_delete=models.CASCADE,blank=True,null=True ,related_name='patient')

    def __str__(self):
        return self.descript()

    def descript(self):
        return f'{self.user.username} Patient'

    def avg_sugar(self):
        all_lvl = [x.level for x in Sugar_level.objects.filter(patient=self)]
        if len(all_lvl) > 0 :
            return f'Średnia to {round((sum(all_lvl) / len(all_lvl)))}'
        else:
            return 'Nie ma wyników'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.descript()

    def descript(self):
        return f'Imię: {self.user.username} - Doktor '
