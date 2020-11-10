from rest_framework.decorators import action
from accounts.models import Account
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from Api.Serializers import AccountCreateSerializer, AccountGetSerializer, PatientListSerializer, \
    PatientDetailSerializer, DoctorGetSerializer, SugarLevelCreateSerializer, CooperateNewSerializer, \
    CooperateGetSerializer, SugarLevelGetSerializer, DoctorListSerializer, \
    CooperateCreateSerializer, AdviceCreateSerializer, AdviceListSerializer, ChatSerializer, RejectCooperateSerializer, ChatNewMessageSerializer

from Api.models import Patient, Doctor, Cooperate, SugarLevel, Advice, Chat, RejectCooperate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db.models import Q
from collections import Counter

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    queryset = Token.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id, 'profile': token.user.get_profile_display()})


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = AccountGetSerializer

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(self.__class__, self).get_permissions()

    def create(self, request, *args, **kwargs):
        if Account.objects.filter(email=request.data['email']).exists():
            return Response("This email address is already being used")
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():

            account = Account.objects.create_user(
                last_name=request.data['last_name'],
                first_name=request.data['first_name'],
                email=request.data['email'],
                age=request.data['age'],
                profile=request.data['profile'],
                phone_number=request.data['phone_number']
            )

            account.set_password(request.data['password'])
            account.save()
            Token.objects.create(user=account)

            if account.profile == '1':
                doctor = Doctor.objects.create(account=account)
                doctor.save()
            else:
                patient = Patient.objects.create(account=account)
                patient.save()

            return Response(serializer.data['email'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PatientDetailSerializer
        else:
            return PatientListSerializer

    @action(detail=False, methods=['post'])
    def my_patient(self, request):
        patients = Patient.objects.filter(doctor=Doctor.objects.get(account__id=request.data['pk']).id)
        out_put = PatientListSerializer(patients, many=True).data
        return Response(out_put)

    def retrieve(self, request, *args, **kwargs):
        serialzier= PatientDetailSerializer(Patient.objects.get(account=kwargs['pk']), many=False).data
        return Response(serialzier, status=status.HTTP_200_OK)

class CooperateViewSet(viewsets.ModelViewSet):
    queryset = Cooperate.objects.all()
    serializer_class = CooperateCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['post'])
    def get_cooperate(self, request):
        out_put = CooperateGetSerializer(
            Cooperate.objects.get(doctor__id=request.data['pk_doctor'], patient__id=request.data['pk_patient'],
                                  is_active=True), many=False).data
        return Response(out_put)

    @action(detail=False, methods=['post'])
    def my_new_cooperate(self, request):
        out_put = CooperateNewSerializer(
            Cooperate.objects.filter(doctor__id=request.data['pk'], rejected=False, is_active=False), many=True).data
        return Response(out_put)

    @action(detail=False, methods=['post'])
    def have_i_sent_cooperate(self, request):
        if Cooperate.objects.filter(patient=request.data['pk']).filter(rejected=False).exists():
            response_obj = CooperateGetSerializer(Cooperate.objects.get(patient=request.data['pk'], rejected=False),
                                                  many=False).data
            response_obj['go_to_doctor_list'] = False
            return Response(response_obj)
        return Response({'go_to_doctor_list': True})


    @action(detail=False, methods=['post'])
    def remove_cooperate(self, request):
        cooperte_obj = Cooperate.objects.get(id=int(request.data['pk']))
        patient = Patient.objects.get(account=cooperte_obj.patient.id)
        patient.doctor = None
        cooperte_obj.rejected = True
        cooperte_obj.is_active = False

        account_how_removed = Account.objects.get(id=request.data['how_removed'])
        send_info_to = 0
        if cooperte_obj.patient.id == request.data['how_removed']:
            send_info_to = cooperte_obj.doctor.id
        else:
            send_info_to = cooperte_obj.patient.id
        account_send_info_to = Account.objects.get(id=send_info_to)
        new_reject_cooperate = RejectCooperate.objects.create(how_rejected=account_how_removed,
                                                              message=f'Cooperate was rejected by {account_how_removed.email}',
                                                              send_info_to=account_send_info_to)

        new_reject_cooperate.save()
        cooperte_obj.save()
        patient.save()
        return Response(status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def reject_cooperate(self, request):
        cooperte_obj = Cooperate.objects.get(id=request.data['pk'])
        cooperte_obj.rejected = True
        account_how_rejected = Account.objects.get(id=request.data['how_rejected'])
        send_info_to = 0
        if cooperte_obj.patient.id == request.data['how_rejected']:
            send_info_to = cooperte_obj.doctor.id
        else:
            send_info_to = cooperte_obj.patient.id
        account_send_info_to = Account.objects.get(id=send_info_to)
        new_reject_cooperate = RejectCooperate.objects.create(how_rejected=account_how_rejected,
                                                              message=f'Cooperate was rejected by {account_how_rejected.email}',
                                                              send_info_to=account_send_info_to )
        new_reject_cooperate.save()
        cooperte_obj.save()
        return Response(status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def activate(self, request):
        cooperate_obj = Cooperate.objects.get(id=request.data['pk'])
        cooperate_obj.is_active = True
        cooperate_obj.accept_doctor = True
        doctor = Doctor.objects.get(account=cooperate_obj.doctor.id)
        patient = Patient.objects.get(account=cooperate_obj.patient.id)
        patient.doctor = doctor
        patient.save()
        cooperate_obj.save()
        return Response(status.HTTP_200_OK)

class RejectCooperateViewSet(viewsets.ModelViewSet):
    queryset = RejectCooperate.objects.all()
    serializer_class = RejectCooperateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['post'])
    def take_all_rejected(self, request):
        list_of_rejected_cooperate = RejectCooperate.objects.filter(send_info_to=request.data['pk'], is_active=True )
        serializer = RejectCooperateSerializer(list_of_rejected_cooperate, many=True).data
        return Response(serializer)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorGetSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, **kwargs):
        doctor = Doctor.objects.get(account_id=request.data['pk'])
        return Response(DoctorGetSerializer(doctor).data)

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer


class SugarLeveViewSet(viewsets.ModelViewSet):
    queryset = SugarLevel.objects.all()
    serializer_class = SugarLevelCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    
    def create(self, request):
        super(SugarLeveViewSet, self).create(request)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def all_info(self, request):
        sugars = SugarLevel.objects.filter(account_id=request.data['pk']).order_by('-date')
        fast_blood_sugars = [sugar.level for sugar in sugars if sugar.without_a_meal is True]

        serializer_list_all = SugarLevelGetSerializer(sugars, many=True)
        avreage_all_sugars = round(sum([sugar.level for sugar in sugars]) / len(sugars)) if len(sugars) > 0 else 0
        avreage_last_five_sugars = round(sum([sugar.level for sugar in sugars[:5]]) / len(sugars[:5])) if len(
            sugars[:5]) > 0 else 0
        avreage_all_fast_blood_sugar = round(sum(fast_blood_sugars) / len(fast_blood_sugars)) if len(
            fast_blood_sugars) > 0 else 0
        out_put = {
            'list_of_all_sugars': serializer_list_all.data,
            'avreage_all_sugars': avreage_all_sugars,
            'avreage_last_five_sugars': avreage_last_five_sugars,
            'avreage_all_fast_blood_sugar': avreage_all_fast_blood_sugar,
        }
        return Response(out_put)
    

class AdviceViewSet(viewsets.ModelViewSet):
    queryset = Advice.objects.all()
    serializer_class = AdviceCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        super(AdviceViewSet, self).create(request)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def for_patient(self,request):
        serializer = AdviceListSerializer(Advice.objects.filter(patient=request.data['pk']),many=True).data
        return Response(serializer)

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['post'])
    def conversation(self, request):
        patientId = request.data['patientId']
        doctorId = request.data['doctorId']

        messages = [x for x in Chat.objects.all().order_by('-date')
                if x.patientId.id == int(doctorId) and x.doctorId.id == int(patientId)
                or x.patientId.id == int(patientId) and x.doctorId.id == int(doctorId)]

        serializer = ChatSerializer(messages, many=True)

        return Response(serializer.data)

class NewElements(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['post'])
    def doctor(self, request):
        pk_form_request = request.data['pk']
        list_cooperate = len(Cooperate.objects.filter(doctor=pk_form_request, rejected=False, is_active=False))
        list_active_cooperate_id = [x.patient for x in Cooperate.objects.filter(doctor=pk_form_request, is_active=True )]
        list_of_chat = Chat.objects.filter(doctorId=pk_form_request, patientId__in=list_active_cooperate_id , is_new=True ).filter(~Q(sender=pk_form_request))
        chat_patient_id_new_msg = [x.patientId.id for x in list_of_chat]
        out_put ={
            'chat_all_new_msg': len(chat_patient_id_new_msg),
            'chat_patient_id_new_msg':dict(Counter(chat_patient_id_new_msg)),
            'list_cooperate':list_cooperate
        }
        return Response(out_put)
