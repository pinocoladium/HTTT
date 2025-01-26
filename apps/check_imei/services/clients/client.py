from typing import Final

import requests
from django.conf import settings


class IMEICheckNetClient:
    BASE_URL: str = settings.IMEI_CHECK_NET_API_URL
    TOKEN: str = settings.IMEI_CHECK_NET_API_TOKEN

    CHECK_IMEI_URL: Final[str] = "/v1/checks"

    def __init__(self, service_id: int) -> None:
        self.service_id = service_id
        self.headers = {"Authorization": f"Bearer {self.TOKEN}"}

    def get_checks(self, imei: str) -> dict:
        url = f"{self.BASE_URL}{self.CHECK_IMEI_URL}"
        try:
            response = requests.post(
                url,
                data={"deviceId": imei, "serviceId": self.service_id},
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
