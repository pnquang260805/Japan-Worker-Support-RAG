from unstructured.documents.elements import Element
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from configs.app_config import AppConfig


class EmbedService:
    def __init__(self):
        conf = AppConfig()
        self.embeddings = HuggingFaceEmbeddings(
            model_name=conf.EMB_MODEL_ID,
            model_kwargs={
                "device": "cuda",
                "processor_kwargs": {"padding_side": "left"},
            },
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_documents(self, texts: list[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)

    def embed_query(self, query: str) -> List[float]:
        return self.embeddings.embed_query(query)