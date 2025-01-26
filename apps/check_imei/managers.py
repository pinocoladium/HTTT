from typing import Final

from apps.check_imei.services.clients.client import IMEICheckNetClient


class CheckImeiManager:
    """
    Менеджер для получения информации по коду IMEI
    """

    SERVICE_ID: Final[int] = 12  # по идее здесь должна быть логики привязки запроса

    def __init__(self, imei: str):
        self.imei = imei

    def get_information(self):
        info = IMEICheckNetClient(self.SERVICE_ID).get_checks(self.imei)
        return info["properties"]
