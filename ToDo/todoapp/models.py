from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class ToDoModel(models.Model):
	CHOICES=(
		('todo','Todo'),
		('inProgress','In progress'),
		('done','Done')
		)
	user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='todolist',on_delete=models.CASCADE,null=True)
	task=models.CharField(max_length=60)
	date=models.DateField()
	time=models.TimeField()
	status=models.CharField(max_length=60,choices=CHOICES,default='todo')
	description=models.TextField(default=None)



class SummaryModel(models.Model):
    taskId=models.ForeignKey(ToDoModel,related_name='todolist',on_delete=models.CASCADE,null=True)
    dateTime=models.DateTimeField(blank=True,default=None)
    description_summary=models.TextField(default='None')
    modefied_detail=models.CharField(max_length=60,default=None,null =True)
    created_update=models.CharField(max_length=60,default=None,null =True)


