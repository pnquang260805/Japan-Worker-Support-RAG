from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import declarative_base

class UserLoginRequest(BaseModel):
    email: str = EmailStr
    password: str = Field(min_length=8)

class UserRegisterRequest(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid4()))
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm : str = Field(min_length=8)
    role: str = Field(default="user")

class UserResponse(BaseModel):
    uid: str
    email: str = EmailStr
    role: str
    redirect_url: str

# ORM
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ =  "user"

    uid: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    role: Mapped[str]

    def __repr__(self):
        return f"<User id={self.uid} name={self.email!r}>"