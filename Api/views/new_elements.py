from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from collections import Counter
from rest_framework.decorators import action

from Api.models import Chat, Cooperate, Advice
from Api.serializers import ChatSerializer

class NewElementsViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['post'])
    def doctor(self, request):
        pk_from_request = request.data['pk']
        list_cooperate = len(Cooperate.objects.filter(doctor=pk_from_request, rejected=False, is_active=False))
        list_active_cooperate_id = [x.patient for x in Cooperate.objects.filter(doctor=pk_from_request, is_active=True)]
        list_of_chat = Chat.objects.filter(doctorId=pk_from_request, patientId__in=list_active_cooperate_id, is_new=True).filter(~Q(sender=pk_from_request))
        chat_patient_id_new_msg = [x.patientId.id for x in list_of_chat]
        out_put = {
            'chat_all_new_msg': len(chat_patient_id_new_msg),
            'chat_patient_id_new_msg': dict(Counter(chat_patient_id_new_msg)),
            'list_cooperate': list_cooperate
        }
        return Response(out_put)

    @action(detail=False, methods=['post'])
    def patient(self, request):
        pk_from_request = request.data['pk']
        new_msg_items = len(Chat.objects.filter(patientId=pk_from_request, is_new=True).filter(~Q(sender=pk_from_request)))
        new_advices = len(Advice.objects.filter(patient=pk_from_request, is_new=True))
        out_put = {
            'new_msg_items': new_msg_items,
            'new_advices': new_advices
        }
        return Response(out_put)