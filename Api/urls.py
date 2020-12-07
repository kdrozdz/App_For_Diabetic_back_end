from django.urls import path
from rest_framework import routers
from Api.views.account import AccountViewSet
from Api.views.cooperate import CooperateViewSet, RejectCooperateViewSet
from Api.views.pateint import PatientViewSet
from Api.views.sugar import SugarLeveViewSet
from Api.views.doctor import DoctorViewSet
from Api.views.advice import AdviceViewSet
from Api.views.chat import ChatViewSet
from Api.views.new_elements import NewElementsViewSet
from Api.views.food import FoodViewSet

from django.conf.urls import include

router = routers.DefaultRouter()
router.register('account', AccountViewSet)
router.register('cooperate', CooperateViewSet)
router.register('reject-cooperate', RejectCooperateViewSet)
router.register('patient', PatientViewSet)
router.register('sugar', SugarLeveViewSet)
router.register('doctor', DoctorViewSet)
router.register('advice', AdviceViewSet)
router.register('chat', ChatViewSet),
router.register('new-elements', NewElementsViewSet),
router.register('food', FoodViewSet),

urlpatterns = (
    path('', include(router.urls)),
)
