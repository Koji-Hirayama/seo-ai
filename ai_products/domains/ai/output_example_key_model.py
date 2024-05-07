from typing import Any, List
from pydantic import BaseModel


class OutputExampleKeyModel(BaseModel):
    key: str
    description: str
    examples: List[Any]
    type: str
