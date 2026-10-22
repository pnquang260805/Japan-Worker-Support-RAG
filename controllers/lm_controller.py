from fastapi import APIRouter, Depends
from interface.language_model import LanguageModel
from models.question_request import QuestionRequest
from langchain_core.vectorstores import VectorStoreRetriever
from models.question_response import QuestionResponse

from common.dependencies import get_lm_service, get_retriever, get_memory_service
from models.question_request import QuestionRequest

router = APIRouter(
    prefix="/lm",
    tags=["LM"]
)


@router.post("/ask", response_model=QuestionResponse)
def ask(question: QuestionRequest, lm_service: LanguageModel = Depends(get_lm_service),
        retriever: VectorStoreRetriever = Depends(get_retriever), memory_service = Depends(get_memory_service)):
    response = lm_service.run_chain(question.question, retriever, memory_service)
    return QuestionResponse(response=response)