from abc import ABC, abstractmethod
from typing import Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever

class LanguageModel(ABC):
    lm: BaseChatModel

    @abstractmethod
    def _create_model(self) -> None:
        pass

    @abstractmethod
    def _build_system_prompt(self) -> None:
        pass

    @abstractmethod
    def run_chain(
        self, question: str, retriever: VectorStoreRetriever, history: Optional[dict]
    ) -> str:
        pass
