from fastapi import APIRouter, Depends
from common.dependencies import get_extractor_service, get_vector_store
from services.extract_service import ExtractService
from configs.app_config import AppConfig
from langchain_text_splitters import RecursiveCharacterTextSplitter
from interface.vector_store import VectorStore

conf = AppConfig()

router = APIRouter(
    prefix="/ingest",
    tags=["Ingest"]
)

@router.post("/")
def ingest(extractor: ExtractService = Depends(get_extractor_service), vector_store: VectorStore = Depends(get_vector_store)):
    print("Bắt đầu load thư mục...")
    raw_docs = extractor.extract_dir(conf.UPLOAD_FOLDER)
    print(f"Đã load xong {len(raw_docs)} trang tài liệu.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    split_docs = text_splitter.split_documents(raw_docs)
    print(f"Đã chia thành {len(split_docs)} đoạn chunks.")
    print("-> Đang embed và nạp vào MongoDB...")
    vector_store.add_documents(split_docs)
    print("Hoàn tất nạp dữ liệu vào MongoDB Atlas!")
    return {"message": "OK"}