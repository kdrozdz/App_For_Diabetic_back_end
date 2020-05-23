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
    date = models.DateTimeField(auto_now=True)
    without_a_meal=models.BooleanField(default=False)
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE  ,related_name='sugar')



class Patient(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor',on_delete=models.CASCADE,blank=True,null=True ,related_name='patient')

    def __str__(self):
        return self.descript()

    def descript(self):
        return f'{self.user.username} Patient'

    def all_sugar(self):
        all_sugar = [x for x in Sugar_level.objects.filter(patient=self)]
        if len(all_sugar) > 0:
            return all_sugar
        return 'Nie ma wyników'

    def avg_sugar(self):
        all_lvl = [x.level for x in Sugar_level.objects.filter(patient=self)]
        if len(all_lvl) > 0 :
            avg_all = round((sum(all_lvl) / len(all_lvl)))
            return avg_all
        else:
            return 'Nie ma wyników'

    def avg_sugar_10(self):
        sugar_10 = Sugar_level.objects.filter(patient=self).order_by('-date')[:10]
        all_lvl=[x.level for x in sugar_10]

        if len(all_lvl) > 0 :
            avg_10 = round((sum(all_lvl) / len(all_lvl)))
            return avg_10
        else:
            return 'Nie ma wyników'


    def avg_no_meal(self):
        sugar_no_meal = [x.level for x in Sugar_level.objects.filter(patient=self).filter(without_a_meal=True)]
        if len(sugar_no_meal) > 0:
            avg_no_meal = round((sum(sugar_no_meal) / len(sugar_no_meal)))
            return avg_no_meal
        else:
            return 'Nie ma wyników'

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.descript()
    def descript(self):
        return f'Imię: {self.user.username} - Doktor '
