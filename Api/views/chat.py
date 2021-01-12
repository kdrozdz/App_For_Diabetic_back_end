from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from Api.models import Chat
from Api.serializers import ChatSerializer


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
        return Response({"conversation": serializer.data,
                         "isLoading": False,
                         })
