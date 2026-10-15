from fastapi import APIRouter, Depends
from interface.language_model import LanguageModel
from models.question_request import QuestionRequest
from langchain_core.vectorstores import VectorStoreRetriever
from models.question_response import QuestionResponse

from common.dependencies import get_lm_service, get_retriever
from models.question_request import QuestionRequest

router = APIRouter(
    prefix="/lm",
    tags=["LM"]
)


@router.post("/ask", response_model=QuestionResponse)
def ask(question: QuestionRequest, lm_service: LanguageModel = Depends(get_lm_service),
        retriever: VectorStoreRetriever = Depends(get_retriever)):
    response = lm_service.run_chain(question.question, retriever)
    return QuestionResponse(response=response)