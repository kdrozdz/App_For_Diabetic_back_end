from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.Serializers import UserSerializer, PatientSerializer ,DoctorSerializer, Sugar_levelSerializer
from Api.models import Patient ,Doctor, Sugar_level


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @action(detail=True,methods=['post'])
    def sugar(self,request,**kwargs):
        new_sugar = Sugar_level.objects.create(patient=self.get_object(),
                                               level=request.data['level'],
                                               without_a_meal=request.data['without_a_meal'],)
        new_sugar.save()
        serializer = PatientSerializer(self.get_object(),many=False)
        return Response(serializer.data)





class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class Sugar_leveViewSet(viewsets.ModelViewSet):
    queryset = Sugar_level.objects.all()
    serializer_class = Sugar_levelSerializer





