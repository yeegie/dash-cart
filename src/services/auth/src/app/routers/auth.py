from fastapi import APIRouter, Body
from app.service.auth import AuthService
from app.schemas.token import TokenSchema


class AuthRouter(APIRouter):
    def __init__(self, service: AuthService):
        super().__init__()
        self.__service = service

        self.add_api_route("/sms", self.send_sms_code, methods=["POST"])
        self.add_api_route("/sms/verify", self.verify_sms_code, methods=["POST"], response_model=TokenSchema)
        self.add_api_route("/token/refresh", self.refresh_token, methods=["POST"], response_model=TokenSchema)
        self.add_api_route("/logout", self.logout, methods=["POST"])

    async def send_sms_code(self, telephone: str = Body(..., embed=True)):
        await self.__service.send_sms_code(telephone)
        return {"message": "SMS sent"}

    async def verify_sms_code(
        self,
        telephone: str = Body(...),
        entered_code: str = Body(...)
    ):
        return await self.__service.verify_sms_code(telephone, entered_code)

    async def refresh_token(self, refresh_token: str = Body(..., embed=True)):
        return await self.__service.refresh_token(refresh_token)

    async def logout(
        self,
        refresh_token: str = Body(..., embed=True),
        all_devices: bool = Body(False)
    ):
        await self.__service.logout(refresh_token, all_devices)
        return {"message": "Logged out"}