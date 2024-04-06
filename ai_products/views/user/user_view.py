from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from ai_products.serializers.user.user_serializer import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
