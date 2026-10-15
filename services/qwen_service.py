from interface.language_model import LanguageModel
from configs.app_config import AppConfig
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate


def _format_docs(docs):
    parts = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "?")
        parts.append(f"[source: {src}, page: {page}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)

class QwenService(LanguageModel):
    def __init__(self):
        conf = AppConfig()
        self._MODEL_ID = conf.LM_MODEL_ID
        self._context_key = "context"
        self._question_key = "question"
        self._api_key = conf.OPEN_AI_API
        self._model_connection_url = conf.MODEL_URL
        self.prompt = None

        self._create_model()

    def _create_model(self):
        self.lm = ChatOpenAI(
            model=self._MODEL_ID,
            api_key=self._api_key,
            temperature=0,
            base_url=self._model_connection_url,
        )

    def _build_system_prompt(self):
        instruct = [
            (
                "system",
                f"""
                You are a strict, citation-focused assistant for a private knowledge base.

                RULES:
                1) Use ONLY the provided context to answer.
                2) If the answer is not clearly contained in the context, say: "I don't know based on the provided documents."
                3) Do NOT use outside knowledge, guessing, or web information.
                4) If applicable, cite sources as (source:page, name:file's name) using the metadata.

                Context:
                {{{self._context_key}}}
                """,
            ),
            ("human", f"{{{self._question_key}}}"),
        ]
        self.prompt = ChatPromptTemplate(instruct)

    def run_chain(self, question, retriever):
        if self.prompt is None:
            self._build_system_prompt()
        parser = StrOutputParser()
        rag_chain = (
            ({self._context_key: retriever | RunnableLambda(_format_docs) , self._question_key: RunnablePassthrough()})
            | self.prompt
            | self.lm
            | parser
        )
        return rag_chain.invoke(question)