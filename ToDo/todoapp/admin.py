from django.contrib import admin
from todoapp.models import ToDoModel,SummaryModel,GroupModel,TaskAssignModel,GroupTaskActivityModel,GroupAdminsModel,GroupTaskAttachmentsModel
# Register your models here.

class ToDoAdmin(admin.ModelAdmin):
    list_display=['user','task','date','time','flagTask']
    list_filter=['task','time','date']

class SummaryAdmin(admin.ModelAdmin):
	list_display=['taskId','description_summary','dateTime']


class GroupAdmin(admin.ModelAdmin):
	list_display = ['id','grpid','member','group','created_by']

class TaskAssignAdmin(admin.ModelAdmin):
	list_display = ['assigned_to_id','assigned_to_name','task','comment','status','assigned_by']


class GroupTaskActivityAdmin(admin.ModelAdmin):
	list_display = ['grpTaskActivity_id','comments','history','dateTime','updated_by']

class GroupAdminsAdmin(admin.ModelAdmin):
	list_display = ['adminUser_id','adminUser']

class GroupTaskAttachmentsAdmin(admin.ModelAdmin):
	list_display = ['fileTask_id','fileName','document','uploaded_at']


admin.site.register(GroupModel,GroupAdmin)

admin.site.register(TaskAssignModel,TaskAssignAdmin)

admin.site.register(GroupTaskActivityModel,GroupTaskActivityAdmin)

admin.site.register(GroupTaskAttachmentsModel,GroupTaskAttachmentsAdmin)

admin.site.register(ToDoModel,ToDoAdmin)

admin.site.register(SummaryModel,SummaryAdmin)

admin.site.register(GroupAdminsModel,GroupAdminsAdmin)
