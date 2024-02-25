from pydantic import BaseModel
from typing import List
from .project_user import ProjectUser as DomainProjectUser

class ProjectUserList(BaseModel):
    project_user_list: List[DomainProjectUser]
    