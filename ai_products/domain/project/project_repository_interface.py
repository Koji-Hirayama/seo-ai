from abc import ABC, abstractmethod
from . import Project as DomainProject
from typing import List

class ProjectRepositoryInterface(ABC):
    @abstractmethod
    def save(self, project: DomainProject) -> DomainProject:
        """Projectの作成とProjectUserの紐付け"""
        pass
        