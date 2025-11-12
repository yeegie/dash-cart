from datetime import datetime, timedelta, timezone
from pathlib import Path
import jwt
from cryptography.hazmat.primitives import serialization
import random
import redis.asyncio as Redis
import logging
import phonenumbers
from app.exceptions.auth_exceptions import InvalidCode, InvalidToken, InvalidPhoneNumber
import secrets
from app.schemas.token import TokenSchema, PayloadSchema
from app.clients.user import UserClient


class AuthService:
    def __init__(
        self,
        redis: Redis,
        user_client: UserClient,
        logger: logging.Logger
    ):
        self.__redis = redis
        self.__user_client = user_client
        self.__logger = logger

        private_key_bytes = Path("secrets/private_key.pem").read_bytes()
        self.__private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
        )
        self.__refresh_secret = Path(
            "secrets/refresh_secret.txt").read_text().strip()

    async def generate_access_token(
        self,
        telephone: str
    ) -> str:
        user = await self.__user_client.get_or_create(telephone)
        now = datetime.now(timezone.utc)
        payload = PayloadSchema(
            iss="http://localhost:8000/auth",
            sub=str(user.id),
            aud="http://localhost:8001/clients",
            iat=now.timestamp(),
            exp=(now + timedelta(hours=24)).timestamp(),
            telephone=telephone
        )
        return jwt.encode(payload=payload.model_dump(), key=self.__private_key, algorithm="RS256")

    async def send_sms_code(self, telephone: str) -> None:
        try:
            code = str(random.randint(1000, 9999))
            self.__logger.info(
                f"   - {telephone} -> sms code: {code} | expire time: {datetime.now() + timedelta(seconds=300)}")

            # *** <== Send SMS ===

            await self.__redis.setex(
                name=f"phone_verify:{telephone}",
                time=300,
                value=code,
            )
        except Exception as ex:
            self.__logger.critical("проёб")
            raise

    async def verify_sms_code(self, telephone: str, entered_code: str) -> TokenSchema:
        stored_code = await self.__redis.get(f"phone_verify:{telephone}")

        if stored_code is None:
            raise InvalidCode(details="Code not found")

        if stored_code == entered_code:
            await self.__redis.delete(f"phone_verify:{telephone}")

            access_token = await self.generate_access_token(telephone)
            refresh_token = secrets.token_urlsafe(32)

            # 7 days
            await self.__redis.setex(f"refresh:{refresh_token}", 7 * 24 * 3600, telephone)

            return TokenSchema(access_token=access_token, refresh_token=refresh_token)
        else:
            raise InvalidCode(details="Incorrect code")

    async def validate_access_token(self, token: str) -> bool:
        public_key_bytes = Path("secrets/public_key.pem").read_bytes()
        public_key = serialization.load_pem_public_key(public_key_bytes)

        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience="http://localhost:8001/clients",
                issuer="http://localhost:8003/auth"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidToken("Token expired", token=token)
        except jwt.InvalidTokenError as e:
            raise InvalidToken(f"Invalid token", token=token)

    async def refresh_token(self, refresh_token: str) -> str:
        telephone = await self.__redis.get(f"refresh:{refresh_token}")
        if telephone is None:
            raise InvalidToken("Invalid or expired refresh token")

        telephone = telephone.decode() if isinstance(telephone, bytes) else telephone

        new_access_token = await self.generate_access_token(telephone)
        new_refresh_token = secrets.token_urlsafe(32)

        await self.__redis.setex(f"refresh:{new_refresh_token}", 7 * 24 * 3600, telephone)
        await self.__redis.delete(f"refresh:{refresh_token}")

        return TokenSchema(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    async def logout(self, refresh_token: str, all_devices: bool = False) -> None:
        await self.__redis.delete(f"refresh:{refresh_token}")

    def _validate_phone(self, phone: str) -> str:
        try:
            parsed = phonenumbers.parse(phone, "RU")
            if not phonenumbers.is_valid_number(parsed):
                raise InvalidPhoneNumber("Invalid phone number")
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except:
            raise InvalidPhoneNumber("Invalid phone number")
