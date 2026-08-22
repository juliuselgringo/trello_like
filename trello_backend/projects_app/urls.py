from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, ColumnViewSet, RegisterView, LoginView, LogoutView
from django.urls import path

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'columns', ColumnViewSet, basename='columns')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
