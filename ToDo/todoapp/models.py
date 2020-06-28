from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


####################This Model is created too store the data of all personal tasks of end user#################################
class ToDoModel(models.Model):
	user=models.ForeignKey(User,related_name='todolist',on_delete=models.CASCADE,null=True)
	task=models.CharField(max_length=60)
	date=models.DateField()
	time=models.TimeField()
	status=models.CharField(max_length=60,default='todo')
	description=models.TextField(default=None)
	flagTask = models.CharField(max_length=60,default='no')


#######################This Model is used too keep record of all updated done in task##############################################
class SummaryModel(models.Model):
    taskId=models.ForeignKey(ToDoModel,related_name='todolist',on_delete=models.CASCADE,null=True)
    dateTime=models.DateTimeField(blank=True,default=None)
    description_summary=models.TextField(default='None')
    modefied_detail=models.CharField(max_length=60,default=None,null =True)
    created_update=models.CharField(max_length=60,default=None,null =True)



#########################This Model is created to store all group belonging too each user#############################################

class GroupModel(models.Model):
	grpid = models.CharField(max_length = 60)
	member =  models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	group =  models.CharField(max_length=60)
	created_by = models.CharField(max_length = 60)

###################This model is used to store the task of each member ###################################################################
class TaskAssignModel(models.Model):
	assigned_to_id = models.ForeignKey(GroupModel,on_delete=models.CASCADE,null=True)
	assigned_to_name = models.CharField(max_length=60)
	task = models.CharField(max_length=60)
	status=models.CharField(max_length=60,default='todo')
	comment=models.TextField(default=None)
	assigned_by = models.CharField(max_length = 60)


##########################This Model is used to keep record of all updates made in task#########################################################
class GroupTaskActivityModel(models.Model):
	grpTaskActivity_id = models.ForeignKey(TaskAssignModel,on_delete=models.CASCADE,null=True)
	comments = models.TextField(default='None')
	history = models.TextField(default='None')
	dateTime=models.DateTimeField(blank=True,default=None)
	updated_by=models.CharField(max_length=60)

######################This Model is used to keep record of all file attachments of task###########################################
class GroupTaskAttachmentsModel(models.Model):
	fileTask_id = models.ForeignKey(TaskAssignModel,on_delete=models.CASCADE,null=True)
	fileName = models.CharField(max_length=60)
	document = models.FileField()
	uploaded_at = models.DateTimeField(auto_now_add=True)

#####################This is used to keep record of all link attachments of task##########################################################
class GroupTaskWebLinkModel(models.Model):
	linkTask_id = models.ForeignKey(TaskAssignModel,on_delete=models.CASCADE,null=True)
	link = models.URLField(max_length=200) 


#######################This model is used to store the admin user##################################################

class GroupAdminsModel(models.Model):
	adminUser_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	adminUser = models.CharField(max_length=60)


