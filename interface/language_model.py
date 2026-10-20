from langchain_core.prompts import ChatPromptTemplate
from abc import ABC, abstractmethod
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chat_models import BaseChatModel


class LanguageModel(ABC):
    @abstractmethod
    def _create_model(self) -> None:
        pass

    @abstractmethod
    def _build_system_prompt(self) -> None:
        pass

    @abstractmethod
    def run_chain(
        self, question: str, retriever: VectorStoreRetriever
    ) -> str:
        pass
