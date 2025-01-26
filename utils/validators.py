from django.core.validators import RegexValidator
from rest_framework import serializers

name_validator = RegexValidator(
    regex=r"^[a-zA-Zа-яёА-ЯЁ\s\-]*$",
)


def _luhn_checksum(card_number):
    """
    Вычисляет контрольную сумму по алгоритму Луна (Luhn algorithm)
    """

    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def validate_imei(value):
    """
    Валидатор для проверки IMEI.
    IMEI должен состоять из 15-17 цифр и проходить проверку контрольной суммы (Luhn algorithm)
    """
    if not value.isdigit():
        raise serializers.ValidationError("IMEI должен содержать только цифры")
    if len(value) != 15:
        raise serializers.ValidationError("IMEI должен состоять из 15 цифр")
    if _luhn_checksum(value) != 0:
        raise serializers.ValidationError("Контрольная сумма IMEI не совпадает")

    return value
