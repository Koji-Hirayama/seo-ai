from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    GetProjectsForUserAPIView,
    CreateProjectAPIView,
    GetTasksForProjectAPIView,
    CreateTaskApiView,
    GetAiTypesAPIView,
    GetWorksForTaskAPIView,
    CreateWorkAPIView,
    AiResponseAPIView,
    ScrapingPromptAiAPIView,
    GetAiModelsAPIView,
    ScrapingResultsAPIView,
    ScrapingPromptMessagesAPIView,
    GetAiTypeInputFieldsAPIView,
    TaskAiAPIView,
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
    # AiType系
    path("v1/get_aitypes/", GetAiTypesAPIView.as_view(), name="get_aitypes"),
    # AiModel系
    path(
        "v1/get_aimodels/",
        GetAiModelsAPIView.as_view(),
        name="get_aimodels",
    ),
    # Task系
    path(
        "v1/<int:project_id>/get_tasks_for_project/",
        GetTasksForProjectAPIView.as_view(),
        name="get_tasks_for_project",
    ),
    # Work系
    path(
        "v1/<int:project_id>/get_works_for_task/",
        GetWorksForTaskAPIView.as_view(),
        name="get_works_for_task",
    ),
    # Ai画面のパーツ系
    path(
        "v1/<int:project_id>/ai/get_ai_type_input_fields/",
        GetAiTypeInputFieldsAPIView.as_view(),
        name="get_ai_type_input_fields",
    ),
    # ==============================
    # POST
    # ==============================
    # Project系
    path("v1/create_project/", CreateProjectAPIView.as_view(), name="create_project"),
    # Task系
    path(
        "v1/<int:project_id>/create_task/",
        CreateTaskApiView.as_view(),
        name="create_task",
    ),
    # Work系
    path(
        "v1/<int:project_id>/create_work/",
        CreateWorkAPIView.as_view(),
        name="create_work",
    ),
    # AI系
    path(
        "v1/<int:project_id>/ai_response/",
        AiResponseAPIView.as_view(),
        name="ai_response",
    ),
    path(
        "v1/<int:project_id>/ai/scraping_prompt_ai/",
        ScrapingPromptAiAPIView.as_view(),
        name="scraping_prompt_ai",
    ),
    path("v1/<int:project_id>/ai/task_ai/", TaskAiAPIView.as_view(), name="task_ai"),
    # スクレイピング単体取得系
    path(
        "v1/scraping_results/",
        ScrapingResultsAPIView.as_view(),
        name="scraping_results",
    ),
    # プロンプトメッセージ取得系
    path(
        "v1/scraping_prompt_message/",
        ScrapingPromptMessagesAPIView.as_view(),
        name="scraping_prompt_message",
    ),
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
