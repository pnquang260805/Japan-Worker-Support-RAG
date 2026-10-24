from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    email: str = EmailStr
    password: str = Field(min_length=8)

class UserRegister(BaseModel):
    email: str = EmailStr
    password: str = Field(min_length=8)
    password_confirm : str = Field(min_length=8)
