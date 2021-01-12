from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from Api.models import Advice
from Api.serializers import AdviceCreateSerializer, AdviceListSerializer


class AdviceViewSet(viewsets.ModelViewSet):
    queryset = Advice.objects.all()
    serializer_class = AdviceCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, **kwargs):
        super(AdviceViewSet, self).create(request)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def for_patient(self, request):
        serializer = AdviceListSerializer(Advice.objects.filter(patient=request.data['pk']), many=True).data
        return Response(serializer)
