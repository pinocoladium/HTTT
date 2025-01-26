from django.urls import path

from api.telegram_bot.views import TGCheckImeiAPIView, TGCheckWhiteListAPIView

urlpatterns = [
    path("check-imei/", TGCheckImeiAPIView.as_view(), name="tg_check_imei"),
    path("white-list/", TGCheckWhiteListAPIView.as_view(), name="tg_white_list"),
]
