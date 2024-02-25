from abc import ABC, abstractmethod
from .project_user_list import ProjectUserList as DomainProjectUserList


class ProjectUserRepositoryInterface(ABC):
    @abstractmethod
    def get_project_user_list_by_user_id(self, user_id: int) -> DomainProjectUserList:
        """指定されたユーザーIDに紐づくProjectUserのリストを取得"""
        