from typing import TYPE_CHECKING

from django.contrib.auth.models import UserManager
from django.db.models import QuerySet

if TYPE_CHECKING:
    from apps.users.models import User


class CustomUserQueryset(QuerySet):
    def list_ids(self) -> list[int]:
        return list(self.values_list("id", flat=True))

    def exclude_id(self, id: int):
        return self.exclude(id=id)


class CustomUserManager(UserManager):
    _queryset_class = CustomUserQueryset

    def create_superuser(self, email, password=None, **extra_fields) -> "User":
        return self.create_user(email, password, **extra_fields)
