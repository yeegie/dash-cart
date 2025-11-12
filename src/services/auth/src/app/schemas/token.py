from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer", examples=["bearer"])


class PayloadSchema(BaseModel):
    iss: str = Field(..., description="Token issuer (e.g., auth service URL)")
    sub: str = Field(..., description="SUBject - unique user UUID")
    aud: str = Field(..., description="Intended audience (e.g., client service URL)")
    iat: float = Field(..., description="Issued at (Unix timestamp)")
    exp: float = Field(..., description="Expiration time (Unix timestamp)")
    scope: str = Field(default="openid", description="Space-separated scopes")

    # Optional
    telephone: str = Field(..., description="User phone number in E.164 format")