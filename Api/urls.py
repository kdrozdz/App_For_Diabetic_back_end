from django.urls import path
from rest_framework import routers
from Api.views import AccountViewSet, PatientViewSet, CooperateViewSet, \
    SugarLeveViewSet, DoctorViewSet, AdviceViewSet, ChatViewSet, RejectCooperateViewSet, NewElements
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('cooperate', CooperateViewSet)
router.register('reject-cooperate', RejectCooperateViewSet)
router.register('patient', PatientViewSet)
router.register('sugar', SugarLeveViewSet)
router.register('doctor', DoctorViewSet)
router.register('advice', AdviceViewSet)
router.register('chat', ChatViewSet),
router.register('new-elements', NewElements),

urlpatterns = (
    path('', include(router.urls)),
)
