from pydantic import BaseModel, EmailStr


class EmailValidation(BaseModel):
    email: EmailStr
    subject: str
    token: str
