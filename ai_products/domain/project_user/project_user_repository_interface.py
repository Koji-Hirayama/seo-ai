from abc import ABC, abstractmethod
from .project_user_list import ProjectUserList as DomainProjectUserList
from .project_user import ProjectUser as DomainProjectUser
from ..user import User as DomainUser


class ProjectUserRepositoryInterface(ABC):
    @abstractmethod
    def get_project_user_list_by_user(self, user: DomainUser) -> DomainProjectUserList:
        """指定されたユーザーIDに紐づくProjectUserのリストを取得"""
        
    @abstractmethod
    def save(self, project_user: DomainProjectUser) -> DomainProjectUser:
        """ProjectUser作成(ユーザーIDとプロジェクトを紐づける)"""