from pydantic import BaseModel,Field
from datetime import datetime
from configs.app_config import AppConfig

class QuestionResponse(BaseModel):
    response_time: str = Field(default_factory=lambda: f"{datetime.now()}")
    response_model: str = Field(default=AppConfig().LM_MODEL_ID)
    response: str