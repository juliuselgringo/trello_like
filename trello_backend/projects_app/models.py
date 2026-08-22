# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Column(models.Model):
    column_id = models.AutoField(primary_key=True)
    column_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'column_'


class Has(models.Model):
    pk = models.CompositePrimaryKey('project_id', 'column_id')
    project = models.ForeignKey('Project', models.DO_NOTHING)
    column_id = models.IntegerField()
    has_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'has_'


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=50)
    project_description = models.CharField(max_length=200, blank=True, null=True)
    project_creation_date = models.DateField()
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'project'


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(unique=True, max_length=50)
    tag_color = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'tag'


class Tagged(models.Model):
    pk = models.CompositePrimaryKey('task_id', 'tag_id')
    task = models.ForeignKey('Task', models.DO_NOTHING)
    tag = models.ForeignKey(Tag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tagged'


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=200)
    task_dead_line = models.DateField(blank=True, null=True)
    column = models.ForeignKey(Column, models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, unique=True)
    user_email = models.CharField(max_length=50, unique=True)
    user_password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user_'
