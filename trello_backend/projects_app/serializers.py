from rest_framework import serializers
from .models import Project, Task, Tagged, Tag, Column, User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'project_description', 'project_creation_date', 'user'] 
        read_only_fields = ['project_id', 'user']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_id', 'tag_name', 'tag_color']

class TaggedSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)

    class Meta:
        model = Tagged
        fields = ['tag']

class TaskSerializer(serializers.ModelSerializer):
    taggeds = TaggedSerializer(many=True, read_only=True, source='tagged_set')

    class Meta:
        model = Task
        fields = ['task_id', 'task_name', 'task_description', 'task_dead_line', 'column', 'project', 'taggeds']

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['column_id', 'column_name'];

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_email', 'user_password'];