import datetime

from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        PermissionsMixin)
from django.db import models

from utils.validators import name_validator

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    username = models.CharField(
        "Логин",
        max_length=20,
        unique=True,
        validators=[AbstractUser.username_validator],
        error_messages={"unique": "Пользователь с таким логином уже существует"},
    )

    password = models.CharField(
        max_length=128,
    )

    first_name = models.CharField(
        "Имя",
        max_length=150,
        validators=[name_validator],
    )

    email = models.EmailField(
        "Email",
        unique=True,
        error_messages={"unique": "Пользователь с таким email уже существует"},
    )

    phone = models.PositiveIntegerField(
        "Номер телефона",
        null=True,
    )

    date_joined = models.DateTimeField(
        "Дата присоединения",
        default=datetime.datetime.now,
    )

    def __str__(self):
        return self.username
