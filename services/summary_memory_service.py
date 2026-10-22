from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain.chat_models import BaseChatModel
from interface.memory import Memory

class SummaryMemory(Memory):
    def __init__(self, llm: BaseChatModel, max_token_limit: int = 500, memory_key: str = "history"):
        self._llm = llm
        self._max_token_limit = max_token_limit
        self._memory_key = memory_key
        self._memories: dict[str, ConversationSummaryBufferMemory] = {}

    def _get_memory(self, session_id: str) -> ConversationSummaryBufferMemory:
        if session_id not in self._memories:
            self._memories[session_id] = ConversationSummaryBufferMemory(
                llm=self._llm,
                max_token_limit=self._max_token_limit,
                memory_key=self._memory_key,
                return_messages=True,  # bắt buộc để dùng với MessagesPlaceholder
            )
        return self._memories[session_id]

    def load_history(self, session_id: str):
        return self._get_memory(session_id).load_memory_variables({})[self._memory_key]

    def save(self, session_id: str, question: str, answer: str) -> None:
        self._get_memory(session_id).save_context({"input": question}, {"output": answer})

    def clear(self, session_id: str) -> None:
        self._memories.pop(session_id, None)