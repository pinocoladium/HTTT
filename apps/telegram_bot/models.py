import datetime

from django.db import models
from django.db.models import QuerySet


class WhiteListTGQueryset(QuerySet):
    pass


class WhiteListTG(models.Model):
    objects = WhiteListTGQueryset.as_manager()

    username = models.CharField(
        "Логин",
        max_length=100,
        blank=True,
    )

    telegram_id = models.PositiveIntegerField(
        "Внутренний номер в телеграме",
        unique=True,
    )

    date_joined = models.DateTimeField(
        "Дата присоединения",
        default=datetime.datetime.now,
    )

    is_blocked = models.BooleanField(
        "Заблокирован",
        default=False,
    )

    def __str__(self):
        return self.username
