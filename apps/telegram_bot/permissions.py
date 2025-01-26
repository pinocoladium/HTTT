from django.conf import settings
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class TGTokenPermission(permissions.BasePermission):
    PERMISSION_TOKEN = settings.PERMISSION_TOKEN

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise PermissionDenied("Отсутствуют заголовки авторизации")
        if not auth_header.startswith("Token "):
            raise PermissionDenied(
                "Неверный формат токена. Должно быть 'Token <token>'."
            )

        token = auth_header.split(" ")[1]

        if token != self.PERMISSION_TOKEN:
            raise PermissionDenied("Неверный токен")

        return True
