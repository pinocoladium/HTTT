from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from apps.check_imei.managers import CheckImeiManager
from apps.telegram_bot.models import WhiteListTG
from apps.telegram_bot.permissions import TGTokenPermission

from .serializers import (TGCheckImeiRequestSerializer,
                          TGCheckWhiteListSerializer)


class TGCheckImeiAPIView(GenericAPIView):
    permission_classes = (TGTokenPermission,)
    check_imei_manager = CheckImeiManager

    def post(self, request):
        serializer = TGCheckImeiRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        information = self.check_imei_manager(
            **serializer.validated_data
        ).get_information()

        return Response(data=information)


class TGCheckWhiteListAPIView(GenericAPIView):
    queryset = WhiteListTG.objects.all()
    permission_classes = (TGTokenPermission,)
    serializer_class = TGCheckWhiteListSerializer

    def get(self, request):
        telegram_id = request.query_params.get("telegram_id")
        instance = get_object_or_404(self.get_queryset(), telegram_id=telegram_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
