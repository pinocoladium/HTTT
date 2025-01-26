from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserCreateAPIView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", UserCreateAPIView.as_view(), name="user_create"),
]
