from django.urls import path
from rest_framework import routers
from Api.views import UsersViewSet ,DoctorViewSet ,PatientViewSet,Sugar_leveViewSet
from django.conf.urls import include


router = routers.DefaultRouter()
router.register('users',UsersViewSet),
router.register('doctors',DoctorViewSet),
router.register('patient',PatientViewSet),
router.register('sugar',Sugar_leveViewSet),

urlpatterns = [
    path('',include(router.urls)),
]
