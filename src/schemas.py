from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    firstname: str = Field('', min_length=2, max_length=20)
    lastname: str = Field('', min_length=2, max_length=20)
    email: EmailStr
    phone: str = Field('', min_length=8, max_length=16)
    birthday: date
    description: str = Field()


class ResponseContact(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: date
    description: str

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
