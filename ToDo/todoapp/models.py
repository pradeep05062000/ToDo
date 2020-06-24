from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class ToDoModel(models.Model):
	user=models.ForeignKey(User,related_name='todolist',on_delete=models.CASCADE,null=True)
	task=models.CharField(max_length=60)
	date=models.DateField()
	time=models.TimeField()
	status=models.CharField(max_length=60,default='todo')
	description=models.TextField(default=None)
	flagTask = models.CharField(max_length=60,default='no')



class SummaryModel(models.Model):
    taskId=models.ForeignKey(ToDoModel,related_name='todolist',on_delete=models.CASCADE,null=True)
    dateTime=models.DateTimeField(blank=True,default=None)
    description_summary=models.TextField(default='None')
    modefied_detail=models.CharField(max_length=60,default=None,null =True)
    created_update=models.CharField(max_length=60,default=None,null =True)




class GroupModel(models.Model):
	grpid = models.CharField(max_length = 60)
	member =  models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	group =  models.CharField(max_length=60)
	created_by = models.CharField(max_length = 60)


class TaskAssignModel(models.Model):
	assigned_to_id = models.ForeignKey(GroupModel,on_delete=models.CASCADE,null=True)
	assigned_to_name = models.CharField(max_length=60)
	task = models.CharField(max_length=60)
	assigned_by = models.CharField(max_length = 60)


