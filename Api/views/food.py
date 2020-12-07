from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


from Api.models import Food
from Api.serializers import FoodListSerializer, FoodCreateSerializer

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('category', 'units', 'patient')
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'list':
            return FoodListSerializer
        return FoodCreateSerializer

    def create(self, request, **kwargs):
        if Food.objects.filter(name=request.data['name'], patient=request.data['patient']).exists():
            return Response('You already have item with this name !')
        super(FoodViewSet, self).create(request)
        return Response('Added')