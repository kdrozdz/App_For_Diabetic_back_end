from rest_framework import serializers
from django.contrib.auth.models import User
from Api.models import Patient ,Doctor ,Sugar_level



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'username', 'password','is_staff')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

class Sugar_levelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sugar_level
        exclude = ['patient','id']

class PatientDetailsSerializer(serializers.ModelSerializer):
    sugar = Sugar_levelSerializer(many=True)
    class Meta:
        model=Patient
        fields=('descript','sugar','avg_sugar')


class DoctorSerializer(serializers.ModelSerializer):
    patient = PatientDetailsSerializer(many=True)
    class Meta:
        model=Doctor
        fields=('descript','id','patient')


class DoctorMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('descript','id')

class PatientSerializer(serializers.ModelSerializer):
    doctor = DoctorMinSerializer(many=False)
    user = UserSerializer(many=False)
    class Meta:
        model=Patient
        fields=('user','id','doctor','avg_sugar','avg_sugar_10',"avg_no_meal")
        depth=1


