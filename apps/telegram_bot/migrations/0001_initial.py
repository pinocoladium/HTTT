# Generated by Django 5.1.5 on 2025-01-25 16:59

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WhiteListTG",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(blank=True, max_length=100, verbose_name="Логин"),
                ),
                (
                    "telegram_id",
                    models.PositiveIntegerField(
                        unique=True, verbose_name="Внутренний номер в телеграме"
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="Дата присоединения"
                    ),
                ),
                (
                    "is_blocked",
                    models.BooleanField(default=False, verbose_name="Заблокирован"),
                ),
            ],
        ),
    ]
