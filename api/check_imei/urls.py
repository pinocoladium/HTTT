from django.urls import path

from .views import CheckImeiAPIView

urlpatterns = [
    path("", CheckImeiAPIView.as_view(), name="check_imei"),
]
