from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from Api.models import Cooperate, Patient, Account, RejectCooperate, Doctor
from Api.serializers import CooperateCreateSerializer, CooperateGetSerializer, CooperateNewSerializer, RejectCooperateSerializer


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
        cooperate_obj = Cooperate.objects.get(id=int(request.data['pk']))
        patient = Patient.objects.get(account=cooperate_obj.patient.id)
        patient.doctor = None
        cooperate_obj.rejected = True
        cooperate_obj.is_active = False
        account_how_removed = Account.objects.get(id=request.data['how_removed'])
        if cooperate_obj.patient.id == request.data['how_removed']:
            send_info_to = cooperate_obj.doctor.id
        else:
            send_info_to = cooperate_obj.patient.id
        account_send_info_to = Account.objects.get(id=send_info_to)
        new_reject_cooperate = RejectCooperate.objects.create(how_rejected=account_how_removed,
                                                              message=f'Cooperate was rejected by {account_how_removed.email}',
                                                              send_info_to=account_send_info_to)

        new_reject_cooperate.save()
        cooperate_obj.save()
        patient.save()
        return Response(status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def reject_cooperate(self, request):
        cooperate_obj = Cooperate.objects.get(id=request.data['pk'])
        cooperate_obj.rejected = True
        account_how_rejected = Account.objects.get(id=request.data['how_rejected'])
        if cooperate_obj.patient.id == request.data['how_rejected']:
            send_info_to = cooperate_obj.doctor.id
        else:
            send_info_to = cooperate_obj.patient.id
        account_send_info_to = Account.objects.get(id=send_info_to)
        new_reject_cooperate = RejectCooperate.objects.create(how_rejected=account_how_rejected,
                                                              message=f'Cooperate was rejected by {account_how_rejected.email}',
                                                              send_info_to=account_send_info_to)
        new_reject_cooperate.save()
        cooperate_obj.save()
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
        list_of_rejected_cooperate = RejectCooperate.objects.filter(send_info_to=request.data['pk'], is_active=True)
        serializer = RejectCooperateSerializer(list_of_rejected_cooperate, many=True).data
        return Response(serializer)
