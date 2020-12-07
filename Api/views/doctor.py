from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from Api.models import Doctor
from Api.serializers import DoctorGetSerializer, DoctorListSerializer


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
