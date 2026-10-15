from pydantic import BaseModel,Field
from datetime import datetime

class QuestionResponse(BaseModel):
    response_time: str = Field(default_factory=lambda: f"{datetime.now()}")
    response: str