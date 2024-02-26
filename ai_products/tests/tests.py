from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status

from ai_products.infrastructure.models import ProjectUser
from ai_products.infrastructure.models import Project
from ai_products.models import User
from ai_products.serializers.project_user import GetProjectsForUserSerializer
from ai_products.domain.project_user import ProjectUserList as DomainProjectUserLis

# Create your tests here.
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
    
    def test_list(self):
        response = self.client.post(
        '/authen/jwt/create/',
        data={
            'email': 'test@gmail.com',
            'password': 'testtesttest',
            }
        )
        print(response.json())
        self.assertTrue('refresh' in response.json().keys())
        self.assertTrue('access' in response.json().keys())
        
        access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        
        url = '/api/v1/get_projects_for_user/'
        response = self.client.get(url)
        
        list = []
        print("===================")
        print(self.user.to_domain())
        print(self.project.to_domain())
        print(self.project_user.to_domain())
        print("===================")
        list.append(self.project_user.to_domain())
        print(list)
        test_data = DomainProjectUserLis(project_user_list=list).model_dump()
        test_data = GetProjectsForUserSerializer(data=test_data).get_data()
        print("=====1======")
        print(response.json())
        print("=====2======")
        print(test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_data)
        
        
    def test_list2(self):
        response = self.client.post(
        '/authen/jwt/create/',
        data={
            'email': 'test@gmail.com',
            'password': 'testtesttest',
            }
        )

        self.assertTrue('refresh' in response.json().keys())
        self.assertTrue('access' in response.json().keys())
        
        access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        
        url = '/api/v1/get_projects_for_user/'
        response = self.client.get(url)
        
        list = []
        list.append(self.project_user.to_domain())

        test_data = DomainProjectUserLis(project_user_list=list).model_dump()
        test_data = GetProjectsForUserSerializer(data=test_data).get_data()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_data)
        