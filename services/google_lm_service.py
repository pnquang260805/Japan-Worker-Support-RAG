from typing import Optional

from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
import os

from configs.app_config import AppConfig
from interface.language_model import LanguageModel
from langchain_google_genai import ChatGoogleGenerativeAI


def _format_docs(docs):
    parts = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        file_name = os.path.basename(src)  # "report.pdf"
        page = d.metadata.get("page", "?")
        parts.append(
            f"[source: {src}, name: {file_name}, page: {page}]\n{d.page_content}"
        )
    return "\n\n---\n\n".join(parts)


class GoogleAI(LanguageModel):
    def __init__(self):
        super().__init__()
        conf = AppConfig()
        self._MODEL_ID = conf.LM_MODEL_ID
        self._context_key = "context"
        self._question_key = "question"
        self._api_key = conf.GOOGLE_API
        print(self._MODEL_ID)
        # self._model_connection_url = conf.MODEL_URL
        self.prompt = None

        self._create_model()

    def _create_model(self) -> None:
        self.lm = ChatGoogleGenerativeAI(
            google_api_key=self._api_key,
            model=self._MODEL_ID,
            model_kwargs={
                "max_token": 2048
            },
            temperature=0.5
        )

    def _build_system_prompt(self) -> None:
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

    def run_chain(
            self, question: str, retriever: VectorStoreRetriever, history: Optional[dict]
    ) -> str:
        if self.prompt is None:
            self._build_system_prompt()
        parser = StrOutputParser()
        rag_chain = (
                {self._context_key: itemgetter("question") | retriever | RunnableLambda(_format_docs),
                 self._question_key: itemgetter("question"),  # Input bây giờ là dict
                 "history": itemgetter("history")  # itemgeter: lấy key trong cái truyền vào
                }
                | self.prompt
                | self.lm
                | parser
        )
        return rag_chain.invoke({"question": question, "history": history})
        # input từ invoke(question) là chuỗi sang {} dạng dict nên cần itemgetter
