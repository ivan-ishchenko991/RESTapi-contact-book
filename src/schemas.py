from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    firstname: str = Field('', min_length=2, max_length=20)
    lastname: str = Field('', min_length=2, max_length=20)
    email: EmailStr
    phone: str = Field('', min_length=8, max_length=16)
    birthday: date
    description: str = Field()


class ResponseUser(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: date
    description: str

    class Config:
        from_attributes = True
