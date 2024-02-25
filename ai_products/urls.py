from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateProjectAPIView, GetProjectsForUserAPIView

router = DefaultRouter()


urlpatterns = [
    path('get_projects_for_user/', GetProjectsForUserAPIView.as_view(), name='get_projects_for_user'),
    path('create_project/', CreateProjectAPIView.as_view(), name='create_project'),
    path('', include(router.urls)),
]