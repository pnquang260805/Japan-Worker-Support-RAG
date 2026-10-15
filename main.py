from services.qwen_service import QwenService
from services.store_service import MongoAtalasStoreService
from services.extract_service import ExtractService
from services.embed_serivce import EmbedService
from configs.app_config import AppConfig

from langchain_text_splitters import RecursiveCharacterTextSplitter

from fastapi import FastAPI
from controllers import file_controller, lm_controller

def asking_lm():
    conf = AppConfig()

    emb_service = EmbedService()
    emb_model = emb_service.embeddings

    vector_store = MongoAtalasStoreService(emb_model)
    lm_service = QwenService()
    extractor = ExtractService()
    retriever = vector_store.retriever

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

    while True:
        question = input(">>>> ").strip()
        print(lm_service.run_chain(question, retriever))

app = FastAPI()
app.include_router(file_controller.router)
app.include_router(lm_controller.router)

# if __name__ == "__main__":
    # asking_lm()