from django.test import TestCase
from parameterized import parameterized
from django.contrib.auth.hashers import make_password
from rest_framework import status

from ai_products.infrastructure.models import ProjectUser
from ai_products.infrastructure.models import Project
from ai_products.models import User
from ai_products.serializers.project_user import GetProjectsForUserSerializer
from ai_products.domain.project_user import ProjectUserList as DomainProjectUserList
from ai_products.domain.project_user import ProjectUser as DomainProjectUser
from ai_products.domain.project import Project as DomainProject
from ai_products.domain.user import User as DomainUser
from ai_products.infrastructure.repository.project_user.project_user_repository import ProjectUserRepository

class TestGetProjectUserListByUser(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        print(f"==TestGetProjectUserListByUser==")
        
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = User.objects.create(
            id=1,
            email='test1@gmail.com',
            password=make_password('testtesttest'),
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        cls.user_2 = User.objects.create(
            id=2,
            email='test2@gmail.com',
            password=make_password('testtesttest'),
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        cls.user_3 = User.objects.create(
            id=3,
            email='test3@gmail.com',
            password=make_password('testtesttest'),
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        cls.project = Project.objects.create(
            name='test',
        )
        cls.project_2 = Project.objects.create(
            name='test2',
        )
        cls.project_user = ProjectUser.objects.create(
            project=cls.project,
            user=cls.user,
            is_admin=True
        )
        cls.project_user_2 = ProjectUser.objects.create(
            project=cls.project_2,
            user=cls.user,
            is_admin=True
        )
        cls.project_user_3 = ProjectUser.objects.create(
            project=cls.project,
            user=cls.user_2,
            is_admin=True
        )
        
        
    @parameterized.expand([
        User(id=1, email="test1@gmail.com", password="testtesttest"),
        User(id=2, email="test2@gmail.com", password="testtesttest"),
        # User(id=3, email="test3@gmail.com", password="testtesttest"),
    ])
    def test_repo(self, user):
        print(f"=test_list=")
        print(f"input: {user.id}")
       
        test_user = user.to_domain()
        repo = ProjectUserRepository()
        result = repo.get_project_user_list_by_user(test_user)
        print(result)
        
        # 対象ユーザーのProjectのみ取得できているかの確認
        for item in result.project_user_list:
            print(item.user.email)
            self.assertEqual(item.user.id, test_user.id)
       