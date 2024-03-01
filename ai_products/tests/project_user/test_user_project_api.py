from rest_framework.test import APITestCase
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

class TestGetProjectsForUserAPIView(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        print(f"==TestGetProjectsForUserAPIView==")
        
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = User.objects.create(
            email='test1@gmail.com',
            password=make_password('testtesttest'),
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        cls.user_2 = User.objects.create(
            email='test2@gmail.com',
            password=make_password('testtesttest'),
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        cls.user_3 = User.objects.create(
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
        
    def auth_token(self, user: User):
        response = self.client.post(
        '/authen/jwt/create/',
        data={
            'email': user.email,
            'password': user.password,
            }
        )
        self.assertTrue('refresh' in response.json().keys())
        self.assertTrue('access' in response.json().keys())
        return response.json().get('access')
    
    @parameterized.expand([
        User(email="test1@gmail.com", password="testtesttest"),
        User(email="test2@gmail.com", password="testtesttest"),
        User(email="test3@gmail.com", password="testtesttest"),
    ])
    def test_list(self, user):
        print(f"=test_list=")
        print(f"input: {user.email}")
        access_token = self.auth_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        
        url = '/api/v1/get_projects_for_user/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if user.email == "test1@gmail.com":
            print("2個以上取得OK")
            self.assertEqual(len(response.data["project_user_list"]), 2)
        elif user.email == "test2@gmail.com":
            print("1個取得OK")
            self.assertEqual(len(response.data["project_user_list"]), 1)
        elif user.email == "test3@gmail.com":
            print("[]: 該当プロジェクトなし")
            self.assertEqual(response.data["project_user_list"], [])
        