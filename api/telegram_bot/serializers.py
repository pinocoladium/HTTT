from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.telegram_bot.models import WhiteListTG
from utils.validators import validate_imei


class TGCheckImeiRequestSerializer(serializers.Serializer):
    imei = serializers.CharField(
        label="IMEI устройства",
        validators=[validate_imei],
    )


class TGCheckWhiteListSerializer(ModelSerializer):
    class Meta:
        model = WhiteListTG
        fields = (
            "username",
            "telegram_id",
            "is_blocked",
        )
