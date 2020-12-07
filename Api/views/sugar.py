from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

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
