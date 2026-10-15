from functools import lru_cache

from services.embed_serivce import EmbedService
from services.store_service import MongoAtalasStoreService
from services.qwen_service import QwenService


@lru_cache
# lru_cache đảm bảo mỗi service chỉ khởi tạo 1 lần (không tạo lại embedding model/kết nối Mongo mỗi request).
def get_vector_store() -> MongoAtalasStoreService:
    emb_model = EmbedService().embeddings
    return MongoAtalasStoreService(emb_model)


@lru_cache
def get_lm_service() -> QwenService:
    return QwenService()


def get_retriever():
    return get_vector_store().retriever