from services.qwen_service import QwenService
from services.store_service import MongoAtalasStoreService
from services.extract_service import ExtractService
from services.embed_serivce import EmbedService
from configs.app_config import AppConfig

from langchain_text_splitters import RecursiveCharacterTextSplitter

from fastapi import FastAPI
from controllers import file_controller, lm_controller, ingest_controller
app = FastAPI()
app.include_router(file_controller.router)
app.include_router(lm_controller.router)
app.include_router(ingest_controller.router)
# if __name__ == "__main__":
    # asking_lm()