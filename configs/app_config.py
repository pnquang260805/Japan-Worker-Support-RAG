from dotenv import load_dotenv
import os

load_dotenv()


class AppConfig:
    def __init__(self):
        self.HUNGGING_FACE_TOKEN = os.getenv("HUNGGING_FACE_TOKEN")
        self.MONGODB_CONNECT_URL = os.getenv("MONGODB_CONNECT_URL")
        self.LM_MODEL_ID = os.getenv("LM_MODEL_ID")
        self.EMB_MODEL_ID = os.getenv("EMB_MODEL_ID", "Qwen/Qwen3-Embedding-0.6B")
        self.MODEL_URL = os.getenv("MODEL_URL")
        if not self.MODEL_URL.endswith("/v1"):
            self.MODEL_URL += "/v1"
        self.OPEN_AI_API = os.getenv("OPEN_AI_API", "not-needed")
        self.DB_NAME = os.getenv("VECTOR_DB_NAME", "vector_db")
        self.ATLAS_COLLECTION = os.getenv("ATLAS_COLLECTION", "atlas_collection")
        self.MONGO_INDEX = os.getenv("MONGO_INDEX", "index")
        self.UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
        self.GOOGLE_API = os.getenv("GOOGLE_API_KEY")