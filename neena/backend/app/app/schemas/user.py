from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, constr, validator

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = "Undefined"


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: constr(min_length=8, max_length=64)


# Properties to receive via API on update
class UserUpdate(UserBase):
    original: constr(min_length=8, max_length=64) = None
    password: constr(min_length=8, max_length=64) = None


class UserInDBBase(UserBase):
    id: UUID
    created_by_email: EmailStr
    modified_by_email: EmailStr

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
