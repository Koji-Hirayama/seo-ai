from abc import ABC, abstractmethod
from .project_user_list import ProjectUserList as DomainProjectUserList
from .project_user import ProjectUser as DomainProjectUser
from ..user import User as DomainUser


class ProjectUserRepositoryInterface(ABC):
    @abstractmethod
    def get_project_user_list_by_user(self, user: DomainUser) -> DomainProjectUserList:
        """_summary_
            指定されたユーザーに紐づくProjectUserのリストを取得
        Args:
            user (DomainUser): ユーザードメイン

        Returns:
            DomainProjectUserList: 指定したユーザーに紐づくProjectUserのリストを返します
        """
        
    @abstractmethod
    def save(self, project_user: DomainProjectUser) -> DomainProjectUser:
        """ProjectUser作成(ユーザーIDとプロジェクトを紐づける)"""
        