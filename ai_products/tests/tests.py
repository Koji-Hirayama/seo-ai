from rest_framework.test import APITestCase
from parameterized import parameterized
from django.contrib.auth.hashers import make_password
from rest_framework import status

from ai_products.infrastructure.models import ProjectUser
from ai_products.infrastructure.models import Project
from ai_products.models import User
from ai_products.serializers.project_user import GetProjectsForUserSerializer
from ai_products.domain.project_user import ProjectUserList as DomainProjectUserLis


# Create your tests here.
# TODO: テストケース作成の試し
class GetProjectsForUserAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(
            email='test@gmail.com',
            password=make_password('testtesttest'),
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        cls.project = Project.objects.create(
            name='test',
        )
        cls.project_user = ProjectUser.objects.create(
            project=cls.project,
            user=cls.user,
            is_admin=True
        )
        
    def auth_token(self):
        response = self.client.post(
        '/authen/jwt/create/',
        data={
            'email': 'test@gmail.com',
            'password': 'testtesttest',
            }
        )
        self.assertTrue('refresh' in response.json().keys())
        self.assertTrue('access' in response.json().keys())
        return response.json().get('access')
    
    def test_list(self):
        
        access_token = self.auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        
        url = '/api/v1/get_projects_for_user/'
        response = self.client.get(url)
        
        list = []
        print("===================")
        print(self.user.to_domain())
        print(self.project.to_domain())
        print(self.project_user.to_domain())
        print("===================")
        project_user = self.project_user.to_domain()
        project_user.project.add_users([self.user.to_domain()])
        list.append(project_user)
        test_data = DomainProjectUserLis(project_user_list=list).model_dump()
        serializer = GetProjectsForUserSerializer(data=test_data)
        serializer.is_valid()
        test_data = serializer.validated_data
        print("=====1======")
        print(response.json())
        print("=====2======")
        print(test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_data)
        
        
    def test_list2(self):
        access_token = self.auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        
        url = '/api/v1/get_projects_for_user/'
        response = self.client.get(url)
        
        list = []
        project_user = self.project_user.to_domain()
        project_user.project.add_users([self.user.to_domain()])
        list.append(project_user)

        test_data = DomainProjectUserLis(project_user_list=list).model_dump()
        serializer = GetProjectsForUserSerializer(data=test_data)
        serializer.is_valid()
        test_data = serializer.validated_data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_data)
        