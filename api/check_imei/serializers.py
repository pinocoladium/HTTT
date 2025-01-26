from rest_framework import serializers

from utils.validators import validate_imei


class CheckImeiRequestSerializer(serializers.Serializer):
    imei = serializers.CharField(
        label="IMEI устройства",
        validators=[validate_imei],
    )
    token = serializers.CharField(
        label="Контракт",
        required=False,
    )
