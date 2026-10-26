from functools import lru_cache

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from services.embed_serivce import EmbedService
from services.file_serivce import FileService
from services.store_service import MongoAtalasStoreService
from services.qwen_service import QwenService
from services.extract_service import ExtractService
from services.google_lm_service import GoogleAI
from interface.language_model import LanguageModel
from interface.memory import Memory
from services.summary_memory_service import SummaryMemory
from services.sqlite_service import SQLiteService
from services.user_service import UserService


@lru_cache
# lru_cache đảm bảo mỗi service chỉ khởi tạo 1 lần (không tạo lại embedding model/kết nối Mongo mỗi request).
def get_vector_store() -> MongoAtalasStoreService:
    emb_model = EmbedService().embeddings
    return MongoAtalasStoreService(emb_model)


@lru_cache
def get_lm_service() -> LanguageModel:
    return GoogleAI()

def get_retriever():
    return get_vector_store().retriever

# Dependency provider (giống @Autowired)
@lru_cache()
def get_file_service() -> FileService:
    return FileService()

@lru_cache()
def get_extractor_service() -> ExtractService:
    return ExtractService()

@lru_cache
def get_memory_service() -> Memory:
    return SummaryMemory(get_lm_service().lm)

@lru_cache
def get_sqlite_service() -> SQLiteService:
    return SQLiteService()

def get_db():
    db = get_sqlite_service().SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)