from django.conf import settings

from django.shortcuts import render
from django.template import response
from rest_framework import viewsets
from .models import Project, Task, Column, User
from .serializers import ProjectSerializer, TaskSerializer, ColumnSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


class RegisterView(APIView):
    def post (self, request):
        user_name = request.data.get('user_name')
        user_email = request.data.get('user_email')
        user_password = request.data.get('user_password')

        if User.objects.filter(user_name=user_name).exists():
            return Response({'error': 'Username already exists'}, status=400)
        if User.objects.filter(user_email=user_email).exists():
            return Response({'error': 'Email already exists'}, status=400)

        try:
            user = User.objects.create(
                user_name=user_name,
                user_email=user_email,
                user_password=make_password(user_password)
            )
            return Response({'message': 'User registered successfully'}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class LoginView(APIView):
    def post(self, request):
        user_name = request.data.get('user_name')
        user_password = request.data.get('user_password')

        try:
            user = User.objects.get(user_name=user_name)
            if not check_password(user_password, user.user_password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=401)

        # Generate JWT token manually (custom User model)
        refresh = RefreshToken()
        refresh['user_id'] = user.user_id
        
        response = Response({'message': 'Login successful'})
        response.set_cookie(
            'access_token', 
            str(refresh.access_token), 
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax'
        )
        return response

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)  # Assuming user_id is the primary key of the User model

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

class ColumnViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        response = Response({'message': 'Logout successful'})
        response.delete_cookie('access_token')
        return response

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user_id': user.user_id,
            'user_name': user.user_name,
            'user_email': user.user_email
        })