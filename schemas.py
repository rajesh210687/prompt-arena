from pydantic import BaseModel
from typing import Literal

class SentimentOutput(BaseModel):
    emotion: Literal["positive", "negative", "neutral"]
