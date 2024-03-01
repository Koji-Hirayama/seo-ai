from rest_framework.test import APITestCase

class BaseTestCase(APITestCase):
    def auth_token(self, email, password):
        response = self.client.post(
        '/authen/jwt/create/',
        data={
            'email': email,
            'password': password,
            }
        )
        self.assertTrue('refresh' in response.json().keys())
        self.assertTrue('access' in response.json().keys())
        return response.json().get('access')