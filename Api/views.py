from accounts.models import Account
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from Api.Serializers import AccountCreateSerializer, AccountGetSerializer, PatientListSerializer,\
    PatientDetailSerializer, CooperateSerializer

from Api.models import Patient, Doctor, Cooperate, Sugar_level, Email
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
        return Response({'token': token.key, 'id': token.user_id, 'profile':token.user.get_profile_display()})


class AccountViewSet (viewsets.ModelViewSet):
    queryset = Account.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    serializer_class = AccountGetSerializer

    def get_permissions(self):
        if self.action in ('create', ):
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(self.__class__, self).get_permissions()


    def create(self, request, *args, **kwargs):
        if(Account.objects.filter(email=request.data['email']).exists()):
            return Response("This email address is already being used")

        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():

            account = Account.objects.create_user(
                last_name=request.data['last_name'],
                first_name=request.data['first_name'],
                email=request.data['email'],
                age=request.data['age'],
                profile=request.data['profile'],
                phone_number=request.data['phone_number'],
            )

            account.set_password(request.data['password'])
            account.save()
            Token.objects.create(user=account)

            if account.profile == '1':
                doctor = Doctor.objects.create(account=account)
                doctor.save()
            elif account.profile == '2':
                patient = Patient.objects.create(account=account)
                patient.save()

            return Response(serializer.data['email'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )


    def retrieve(self, request, pk=None, **kwargs):
        patient = Patient.objects.get(account_id=pk)
        return Response(PatientDetailSerializer(patient).data)


class CooperateViewSet(viewsets.ModelViewSet):
    queryset = Cooperate.objects.all()
    serializer_class = CooperateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    def update(self, request, *args, **kwargs):
        cooperate_realation = self.get_object()

        if cooperate_realation.accept_sender == True and cooperate_realation.accept_reciver == True:
            cooperate_realation.is_active = True

        if cooperate_realation.rejected == True:
            cooperate_realation.is_active = False



            # sender = models.ForeignKey(Account, related_name='user_sender_cooperate', on_delete=models.DO_NOTHING)
            # reciver = models.ForeignKey(Account, related_name='user_reciver_cooperate', on_delete=models.DO_NOTHING)
            # accept_sender = models.BooleanField(default=False)
            # accept_reciver = models.BooleanField(default=False)
            # is_active = models.BooleanField(default=False)
    # def all_sugar(self):
    #     all_sugar = [x for x in Sugar_level.objects.filter(patient=self)]
    #     if len(all_sugar) > 0:
    #         return all_sugar
    #
    # def avg_sugar(self):
    #     all_lvl = [x.level for x in Sugar_level.objects.filter(patient=self)]
    #     if len(all_lvl) > 0:
    #         avg_all = round((sum(all_lvl) / len(all_lvl)))
    #         return avg_all
    #     else:
    #         return 'Nie ma wyników'
    #
    # def avg_sugar_10(self):
    #     sugar_10 = Sugar_level.objects.filter(patient=self).order_by('-date')[:10]
    #     all_lvl = [x.level for x in sugar_10]
    #
    #     if len(all_lvl) > 0:
    #         avg_10 = round((sum(all_lvl) / len(all_lvl)))
    #         return avg_10
    #     else:
    #         return 'Nie ma wyników'
    #
    # def retrieve(self, request, pk=None, **kwargs):
    #     try:
    #         serializer = PatientSerializer(Patient.objects.get(user_id=pk))
    #         return Response(serializer.data)
    #     except:
    #         return Response("")
    #
    # @action(detail=True, methods=['post'])
    # def sugar(self, request, pk=None, **kwargs):
    #     patient = Patient.objects.get(user_id=pk)
    #     new_sugar = Sugar_level.objects.create(patient=patient,
    #                                            level=request.data['level'],
    #                                            without_a_meal=request.data['without_a_meal'])
    #     serializer = SugarLevelSerializer(new_sugar.save(), many=False)
    #     return Response(serializer.data)
    #
    # def list(self, request, *args, **kwargs):
    #     pateint = Patient.objects.filter(doctor=None)
    #     serializer = PatientDetailsSerializer(pateint, many=True)
    #     return Response(serializer.data)
#
#
# class DoctorViewSet(viewsets.ModelViewSet):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     def retrieve(self, request, pk=None, **kwargs):
#         instance = Doctor.objects.get(user_id=pk)
#         serializer = DoctorSerializer(instance)
#         return Response(serializer.data)
#
#     @action(detail=True, methods=['post'])
#     def add_patient(self, request, pk=None, **kwargs):
#         doctor = Doctor.objects.get(user_id=pk)
#         patients = Patient.objects.get(user_id=request.data['patient_pk'])
#         patients.doctor = doctor
#         patients.save()
#         serializer = PatientDetailsSerializer(patients)
#         return Response(serializer.data)
#
#     @action(detail=True)
#     def my_patients(self, request, *args, pk=None, **kwargs):
#         patients = Patient.objects.filter(doctor__user=pk)
#         serializer = PatientDetailsSerializer(patients, many=True)
#         return Response(serializer.data)
#
#     @action(detail=False, methods=['post'])
#     def rm_patient(self, request, *args, **kwargs):
#         patient = Patient.objects.get(user=request.data.get('userId'))
#         patient.doctor = None
#         patient.save()
#         return Response(None)
#
#
# class SugarLeveViewSet(viewsets.ModelViewSet):
#     queryset = Sugar_level.objects.all()
#     serializer_class = SugarLevelSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     def list(self, request, *args, **kwargs):
#         sugars = Sugar_level.objects.filter(patient__user=request.query_params.get('pk')).order_by('-date')
#         serializer = SugarLevelSerializer(sugars, many=True)
#         return Response(serializer.data)
#
#
# class EmailViewSet(viewsets.ModelViewSet):
#     queryset = Email.objects.all()
#     serializer_class = EmailSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     def update(self, request, *args, **kwargs):
#         msg = self.get_object()
#         msg.is_new = request.data.get('is_new')
#         msg.save()
#         return Response("ok")
#
#     @action(detail=False, methods=['post'])
#     def conv(self, request, *args, **kwargs):
#         rec = request.data['rId']
#         send = request.data['sId']
#         msg = [x for x in Email.objects.all().order_by('-create_time')
#                 if x.sender.id == int(send) and x.reciver.id == int(rec)
#                 or x.sender.id == int(rec) and x.reciver.id == int(send)]
#         serializer = EmailSerializer(msg, many=True)
#         return Response(serializer.data)
#
#     @action(detail=False, methods=['post'])
#     def new_msg(self, request, *args, **kwargs):
#         msg = Email.objects.filter(reciver=request.data['rId']).filter(is_new=True)
#         serializer = EmailSerializer(msg, many=True)
#         return Response(serializer.data)
