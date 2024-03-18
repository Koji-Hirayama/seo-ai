from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GetProjectsForUserAPIView,
    CreateProjectAPIView,
    GetTasksForProjectAPIView,
    CreateTaskApiView,
    GetAiTypesAPIView,
)
from .views import LoginView, LogoutView, RefreshTokenView, TokenVerifyView

router = DefaultRouter()


urlpatterns = [
    # ==============================
    # GET
    # ==============================
    # Project系
    path(
        "v1/get_projects_for_user/",
        GetProjectsForUserAPIView.as_view(),
        name="get_projects_for_user",
    ),
    # Task系
    path(
        "v1/get_tasks_for_project/",
        GetTasksForProjectAPIView.as_view(),
        name="get_tasks_for_project",
    ),
    # AiType系
    path("v1/get_aitypes/", GetAiTypesAPIView.as_view(), name="get_aitypes"),
    # ==============================
    # POST
    # ==============================
    # Project系
    path("v1/create_project/", CreateProjectAPIView.as_view(), name="create_project"),
    # Task系
    path("v1/create_task/", CreateTaskApiView.as_view(), name="create_task"),
    # ==============================
    # 認証関係
    # ==============================
    # path("v1/authen/", include("djoser.urls.jwt")),  # token獲得用
    # 認証カスタム系
    path("v1/login/", LoginView.as_view(), name="login"),
    path("v1/logout/", LogoutView.as_view(), name="logout"),
    path("v1/token_verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("v1/token_refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    # ==============================
    # ViewSet系
    # ==============================
    path("v1/", include(router.urls)),
]
