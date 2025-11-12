import httpx
from typing import Optional
from pydantic import BaseModel, Field
from .schemas import UserSchema, GetUserSchema, GetUsersSchema
import logging


class UserClientError(Exception):
    """Базовое исключение для ошибок UserService"""
    pass


class UserClient:
    def __init__(self, base_url: str, logger: logging.Logger, timeout: float = 5.0):
        self.__base_url = base_url
        self.__logger = logger

        self.__client = httpx.AsyncClient(
            base_url=self.__base_url,
            timeout=timeout,
            # transport=httpx.AsyncHTTPTransport(retries=3)
        )

    async def get_or_create(self, telephone: str) -> GetUserSchema:
        self.__logger.info(f"[i] POST -> {self.__base_url + '/users/get-or-create'}")
        try:
            response = await self.__client.post(
                "/users/get-or-create",
                json={"telephone": telephone}
            )
            response.raise_for_status()
            data = response.json()
            return GetUserSchema(**data)
        except httpx.HTTPStatusError as e:
            self.__logger.error(f"UserService вернул ошибку: {e.response.status_code} {e.response.text}")
            raise UserClientError(f"UserService error: {e.response.status_code}") from e

        except httpx.RequestError as e:
            self.__logger.error(f"Ошибка сети при вызове UserService: {e}")
            raise UserClientError("UserService недоступен") from e

        except (ValueError, KeyError) as e:
            self.__logger.error(f"UserService вернул некорректный ответ: {e}")
            raise UserClientError("Invalid response from UserService") from e

    async def close(self):
        await self.__client.aclose()
