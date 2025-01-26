from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.check_imei.managers import CheckImeiManager

from .serializers import CheckImeiRequestSerializer


class CheckImeiAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    check_imei_manager = CheckImeiManager

    def post(self, request):
        serializer = CheckImeiRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        information = self.check_imei_manager(
            **serializer.validated_data
        ).get_information()

        return Response(data=information)
