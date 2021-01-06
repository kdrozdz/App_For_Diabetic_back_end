from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from Api.models import Patient, Doctor
from Api.serializers import PatientListSerializer, PatientDetailSerializer


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
        serialzier = PatientDetailSerializer(Patient.objects.get(account=kwargs['pk']), many=False).data
        return Response(serialzier, status=status.HTTP_200_OK)
