from django.urls import path
from rest_framework import routers
from Api.views import AccountViewSet, PatientViewSet, CooperateViewSet, SugarLeveViewSet, DoctorViewSet
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('cooperate', CooperateViewSet)
router.register('patient', PatientViewSet)
router.register('sugar', SugarLeveViewSet)
router.register('doctor', DoctorViewSet)
# router.register('email',EmailViewSet),

urlpatterns = (
    path('', include(router.urls)),
)
