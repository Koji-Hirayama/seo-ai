from pydantic import BaseModel
from ai_products.domain.project import Project as DomainProject
from ai_products.domain.user import User as DomainUser

class ProjectUser(BaseModel):
    id: int
    user: DomainUser
    project: DomainProject
    is_admin: bool