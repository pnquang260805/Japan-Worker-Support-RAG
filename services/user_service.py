import email

from fastapi import HTTPException

import bcrypt
from models.user import UserLoginRequest, UserRegisterRequest, User, UserResponse
from sqlalchemy.orm import Session
from configs.app_config import AppConfig

conf = AppConfig()

class UserService:
    def __init__(self, db: Session): # Không tạo SQLiteService
        self.db = db

    def get_by_email(self, email: str) -> User | None: # Bảng user
        return self.db.query(User).filter(User.email == email).first()

    def register(self, register: UserRegisterRequest) -> User:
        if self.get_by_email(register.email) is not None:
            raise HTTPException(409, "Email đã tồn tại")
        hashed = bcrypt.hashpw(register.password.encode(), conf.BCRYPT_SALT)
        user = User(uid=register.uid, email=register.email, password=hashed, role=register.role)
        self.db.add(user)
        self.db.flush()
        return user

    def login(self, request: UserLoginRequest) -> User:
        user = self.get_by_email(request.email)
        if not user or not bcrypt.checkpw(request.password.encode(), user.password.encode()):
            raise HTTPException(401, "Sai email hoặc mật khẩu")
        return user