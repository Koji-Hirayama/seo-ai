from pydantic import BaseModel
from datetime import datetime
from typing import List
from ..ai_type import AiType as DomainAiType
from ..project import Project as DomainProject
from ..user import User as DomainUser

class Task(BaseModel):
    name: str
    description: str
    ai_type: DomainAiType
    project: DomainProject
    user: DomainUser
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None