from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class RefreshTokenBase(BaseModel):
    token: str
    is_valid: bool = True


class RefreshTokenCreate(RefreshTokenBase):
    pass


class RefreshTokenUpdate(RefreshTokenBase):
    is_valid: bool = Field(..., description="Deliberately disable a refresh token.")


class RefreshToken(RefreshTokenUpdate):
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
    refresh: Optional[bool] = False


class WebToken(BaseModel):
    claim: str
