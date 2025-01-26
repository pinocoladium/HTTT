import os
from typing import Final

import aiohttp

BASE_API_URL: Final[str] = "http://django:8000/api/telegram-bot"
CHECK_IMEI_URL: Final[str] = "/check-imei/"
WHITE_LIST_URL: Final[str] = "/white-list/"
HEADERS: Final[dict] = {"Authorization": f"Token {os.getenv('PERMISSION_TOKEN')}"}


async def check_user_in_whitelist(telegram_id: int) -> bool | None:
    async with aiohttp.ClientSession() as session:

        url = f"{BASE_API_URL}{WHITE_LIST_URL}"
        data = {"telegram_id": telegram_id}

        async with session.get(url, params=data, headers=HEADERS) as response:
            if response.status == 200:
                response = await response.json()
                if response.get("is_blocked") is False:
                    return True
            elif response.status == 404:
                return False


async def add_to_whitelist(username: str, telegram_id: int) -> bool:
    async with aiohttp.ClientSession() as session:

        url = f"{BASE_API_URL}{WHITE_LIST_URL}"
        data = {"username": username, "telegram_id": telegram_id}

        async with session.post(url, data=data, headers=HEADERS) as response:
            if response.status == 201:
                return True
            else:
                return False


async def check_imei(imei: int) -> tuple | None:
    async with aiohttp.ClientSession() as session:

        data = {"imei": imei}
        url = f"{BASE_API_URL}{CHECK_IMEI_URL}"

        async with session.post(url, json=data, headers=HEADERS) as response:
            if response.status in (200, 400):
                response_data = await response.json()
                response_text = "\n".join(
                    [f"{key}: {value}" for key, value in response_data.items()]
                )
                return (response.status, response_data)
