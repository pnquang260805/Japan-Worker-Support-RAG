from models.user import Base
from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import sessionmaker
from configs.app_config import AppConfig

conf = AppConfig()

class SQLiteService:
    def __init__(self):
        self.engine = create_engine(
            conf.SQLITE_PATH,
            connect_args={"check_same_thread": False},
            echo=True
        )
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False)
        self.init_db()

    def init_db(self):
        Base.metadata.create_all(self.engine, checkfirst=True) # Tạo bảng