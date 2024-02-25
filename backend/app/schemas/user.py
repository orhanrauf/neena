from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, constr, validator

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = "Undefined"
    auth0_id: str

# Properties to receive via API on creation
class UserCreate(UserBase):
    pass

# Properties to receive via API on update
class UserUpdate(UserBase):
    permissions: Optional[list[str]] = None

class UserInDBBase(UserBase):
    id: UUID
    permissions: Optional[list[str]] = None
    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    hashed_password: bool = Field(default=False, alias="password")

    class Config:
        populate_by_name = True

    @validator("hashed_password", pre=True)
    def evaluate_hashed_password(cls, hashed_password):
        if hashed_password:
            return True
        return False


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None
