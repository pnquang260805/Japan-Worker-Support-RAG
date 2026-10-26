from uuid import uuid4

import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.user import User


def seed_admin(db: Session, email: str, password: str) -> None:
    if db.query(User).filter(User.email == email).first():
        return  # đã có thì bỏ qua

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.add(User(uid=str(uuid4()), email=email, password=hashed, role="admin"))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()  # trường hợp nhiều worker cùng seed một lúc