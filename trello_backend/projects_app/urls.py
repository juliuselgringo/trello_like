from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, ColumnViewSet, RegisterView, LoginView
from django.urls import path

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'columns', ColumnViewSet, basename='columns')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls
