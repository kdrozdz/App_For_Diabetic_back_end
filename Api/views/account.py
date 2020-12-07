from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication

from Api.models import Account, Doctor, Patient
from Api.serializers import AccountGetSerializer, AccountCreateSerializer


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
