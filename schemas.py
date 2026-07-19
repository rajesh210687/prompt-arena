from pydantic import BaseModel, ConfigDict 
from typing import Literal

class SentimentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    emotion: Literal["positive", "negative", "neutral"]
