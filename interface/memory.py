from abc import ABC, abstractmethod
from langchain_classic.memory import ConversationSummaryBufferMemory

class Memory(ABC):
    @abstractmethod
    def _get_memory(self, session_id: str) -> ConversationSummaryBufferMemory:
        pass

    @abstractmethod
    def load_history(self, session_id: str):
        pass

    @abstractmethod
    def save(self, session_id: str, question: str, answer: str) -> None:
        pass

    @abstractmethod
    def clear(self, session_id: str) -> None:
        pass