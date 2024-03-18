from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from ai_products.serializers.user.user_serializer import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


# class TokenObtainView(jwt_views.TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except jwt_exp.TokenError as e:
#             raise jwt_exp.InvalidToken(e.args[0])

#         res = response.Response(serializer.validated_data, status=status.HTTP_200_OK)
#         try:
#             res.delete_cookie("user_token")
#         except Exception as e:
#             print(e)  # ここら辺適当すぎる

#         # httpOnlyなのでtokenの操作は全てdjangoで行う
#         res.set_cookie(
#             "user_token",
#             serializer.validated_data["access"],
#             max_age=60 * 60 * 24,
#             httponly=True,
#         )
#         res.set_cookie(
#             "refresh_token",
#             serializer.validated_data["refresh"],
#             max_age=60 * 60 * 24 * 30,
#             httponly=True,
#         )
#         return res
