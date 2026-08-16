from django.conf import settings

from django.shortcuts import render
from django.template import response
from rest_framework import viewsets
from .models import Project, Task, Column, User
from .serializers import ProjectSerializer, TaskSerializer, ColumnSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
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
