from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from Api.Serializers import UserSerializer, PatientSerializer ,DoctorSerializer, Sugar_levelSerializer
from Api.models import Patient ,Doctor, Sugar_level
from rest_framework.permissions import IsAuthenticated, AllowAny



class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.create_user(username=request.data['username'],
                                                   is_staff=request.data['is_staff'],)
            user.set_password(request.data['password'])
            user.save()
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except:
            return Response("Użytkownik juz istnieje")


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


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
    permission_classes=(IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    @action(detail=True)
    def add_patient(self,request,**kwargs):
        doctor = self.get_object()
        patients= Patient.objects.get(pk=request.data['patient_pk'])
        patients.doctor = doctor
        patients.save()

        serializer = PatientSerializer(patients,many=True)
        return Response(serializer.data)

class Sugar_leveViewSet(viewsets.ModelViewSet):
    queryset = Sugar_level.objects.all()
    serializer_class = Sugar_levelSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)







