from django.urls import include, path

urlpatterns = [
    path("users/", include("api.users.urls")),
    path("check-imei/", include("api.check_imei.urls")),
    path("telegram-bot/", include("api.telegram_bot.urls")),
]
