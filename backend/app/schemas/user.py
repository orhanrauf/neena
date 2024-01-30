from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, constr, validator

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = "Undefined"


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    auth0_id: str
    permissions: Optional[list[str]] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    permissions: Optional[list[str]]


class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    hashed_password: bool = Field(default=False, alias="password")

    class Config:
        allow_population_by_field_name = True

    @validator("hashed_password", pre=True)
    def evaluate_hashed_password(cls, hashed_password):
        if hashed_password:
            return True
        return False


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None
