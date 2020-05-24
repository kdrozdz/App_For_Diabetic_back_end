from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from Api.Serializers import UserSerializer, PatientSerializer ,DoctorSerializer, Sugar_levelSerializer ,PatientDetailsSerializer ,EmailSerializer
from Api.models import Patient ,Doctor, Sugar_level , Email
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    queryset = Token.objects.all()
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id':token.user_id})


class UsersViewSet ( viewsets.ModelViewSet ) :
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

    def retrieve(self, request, pk=None, **kwargs):
        instance = Patient.objects.get(user_id=pk)
        serializer = PatientSerializer(instance)
        return Response(serializer.data)


    @action(detail=True,methods=['post'])
    def sugar(self,request,pk=None,**kwargs):
        patient = Patient.objects.get(user_id=pk)
        new_sugar = Sugar_level.objects.create(patient=patient,
                                               level=request.data['level'],
                                               without_a_meal=request.data['without_a_meal'],)
        new_sugar.save()
        serializer = Sugar_levelSerializer(new_sugar,many=False)
        return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        pateint = Patient.objects.filter(doctor=None)
        serializer = PatientDetailsSerializer(pateint , many=True)
        return  Response(serializer.data)



class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None,**kwargs):
        instance = Doctor.objects.get(user_id=pk)
        serializer = DoctorSerializer(instance)
        return Response(serializer.data)

    @action(detail=True , methods=['post'])
    def add_patient(self,request,pk=None,**kwargs):
        doctor = Doctor.objects.get(user_id=pk)
        patients= Patient.objects.get(user_id=request.data['patient_pk'])
        patients.doctor = doctor
        patients.save()
        serializer = PatientDetailsSerializer(patients)
        return  Response(serializer.data)

    @action(detail=True)
    def my_patients(self,request, *args ,pk=None , **kwargs):
        patients = Patient.objects.filter(doctor__user=pk)
        serializer = PatientDetailsSerializer(patients,many=True)
        return Response(serializer.data)

    @action(detail=False , methods=['post'])
    def rm_patient(self,request,*args,**kwargs):
        patient = Patient.objects.get(user=request.data.get('userId'))
        patient.doctor = None
        patient.save()
        return Response(None)

class Sugar_leveViewSet(viewsets.ModelViewSet):
    queryset = Sugar_level.objects.all()
    serializer_class = Sugar_levelSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        sugars = Sugar_level.objects.filter(patient__user=request.query_params.get('pk')).order_by('-date')
        serializer = Sugar_levelSerializer(sugars,many=True)
        return Response(serializer.data)

class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=False ,methods=['post'])
    def conv(self,request, *args,**kwargs):
        iSend = Email.objects.filter(sender=request.data['sId']).filter(reciver=request.data.get('rId')).order_by('-create_time')
        serializer = EmailSerializer(iSend,many=True)
        return Response(serializer.data)






