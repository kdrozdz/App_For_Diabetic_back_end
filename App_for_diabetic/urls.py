from django.contrib import admin
from django.urls import path, include
from Api.views import CustomObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Api.urls')),
    path('auth/', CustomObtainAuthToken.as_view()),
]
