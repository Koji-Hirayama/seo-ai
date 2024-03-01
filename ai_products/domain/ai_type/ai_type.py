from pydantic import BaseModel
from datetime import datetime

class AiType(BaseModel):
    name: str
    description: str
    created_at: datetime | None = None