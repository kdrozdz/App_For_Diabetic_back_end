from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from django.db.models import Avg
from django.db.models.functions import Round
from django.db.models.functions import Coalesce

from Api.models import SugarLevel
from Api.serializers import SugarLevelCreateSerializer, SugarLevelGetSerializer


class SugarLeveViewSet(viewsets.ModelViewSet):
    queryset = SugarLevel.objects.all()
    serializer_class = SugarLevelCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, **kwargs):
        super(SugarLeveViewSet, self).create(request)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def all_info(self, request):

        serializer_list_all = SugarLevelGetSerializer(SugarLevel.objects.filter(account_id=request.data['pk'])
                                                      .order_by('-date'), many=True)
        avreage_all_sugars = SugarLevel.objects.filter(account_id=request.data['pk'])\
            .aggregate(avg=Round(Coalesce(Avg('level'), 0)))
        avreage_last_five_sugars = SugarLevel.objects.filter(account_id=request.data['pk']).order_by('-date')[:5]\
            .aggregate(avg=Round(Coalesce(Avg('level'), 0)))
        avreage_all_fast_blood_sugar = SugarLevel.objects.filter(account_id=request.data['pk'], without_a_meal=True)\
            .aggregate(avg=Round(Coalesce(Avg('level'), 0)))

        return Response({
            'list_of_all_sugars': serializer_list_all.data,
            'avreage_all_sugars': int(avreage_all_sugars['avg']),
            'avreage_last_five_sugars': int(avreage_last_five_sugars['avg']),
            'avreage_all_fast_blood_sugar': int(avreage_all_fast_blood_sugar['avg']),
        })
