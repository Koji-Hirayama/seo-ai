from pydantic import BaseModel
from datetime import datetime
from typing import List
from ai_products.domain.user import User as DomainUser

class Project(BaseModel):
    id: int
    name: str
    users: List[DomainUser]
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    
    
    def hoge():
        print("ホゲホゲ")
    