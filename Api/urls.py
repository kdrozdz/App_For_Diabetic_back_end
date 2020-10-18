from django.urls import path
from rest_framework import routers
from Api.views import AccountViewSet, PatientViewSet, CooperateViewSet
from django.conf.urls import include
from django.conf.urls import url



router = routers.DefaultRouter()
router.register('accounts', AccountViewSet),
router.register('cooperate', CooperateViewSet),
# router.register('doctors',DoctorViewSet),
router.register('patient',PatientViewSet),
# router.register('sugar',SugarLeveViewSet),
# router.register('email',EmailViewSet),



urlpatterns = (
    path('', include(router.urls)),
)
