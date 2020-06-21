from django.contrib import admin
from todoapp.models import ToDoModel,SummaryModel
# Register your models here.

class ToDoAdmin(admin.ModelAdmin):
    list_display=['user','task','date','time','flagTask']
    list_filter=['task','time','date']

class SummaryAdmin(admin.ModelAdmin):
	list_display=['taskId','description_summary','dateTime']



admin.site.register(ToDoModel,ToDoAdmin)

admin.site.register(SummaryModel,SummaryAdmin)
