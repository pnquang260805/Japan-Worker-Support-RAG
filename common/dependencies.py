from functools import lru_cache

from services.embed_serivce import EmbedService
from services.file_serivce import FileService
from services.store_service import MongoAtalasStoreService
from services.qwen_service import QwenService
from services.extract_service import ExtractService

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

# Dependency provider (giống @Autowired)
@lru_cache()
def get_file_service() -> FileService:
    return FileService()

@lru_cache()
def get_extractor_service() -> ExtractService:
    return ExtractService()