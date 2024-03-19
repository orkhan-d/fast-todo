from pydantic import BaseModel, validator

from api.auth.crud import get_user_by_email

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str

    @validator('email')
    def check_email_exists(cls, value: str):
        if get_user_by_email(value):
            raise ValueError('Given email already exists!')
        return value

class RecoverPasswordSchema(BaseModel):
    email: str