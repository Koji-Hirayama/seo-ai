from pydantic import BaseModel
from datetime import datetime
from typing import List
from ai_products.domain.user import User as DomainUser

class Project(BaseModel):
    id: int | None = None
    name: str
    users: List[DomainUser] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    
    def add_users(self, users: List[DomainUser]) -> "Project":
        self.users = users
        return self
    
    