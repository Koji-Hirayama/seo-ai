from pydantic import BaseModel
from datetime import datetime
from typing import List
from ai_products.domain.user import User as DomainUser
from ai_products.domain.task import Task as DomainTask

class Project(BaseModel):
    id: int | None = None
    name: str
    users: List[DomainUser] | None = None
    tasks: List[DomainTask] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    
    def add_users(self, users: List[DomainUser]) -> "Project":
        self.users = users
        return self
    
    def add_tasks(self, tasks: List[DomainTask]) -> "Project":
        self.tasks = tasks
        return self
    
    