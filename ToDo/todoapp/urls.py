from ToDo import settings
from django.conf.urls.static import static

from django.urls import path,re_path
from todoapp import views as v1            

urlpatterns = [
    path('',v1.todo_create_view),
    path('signup/',v1.signup_view),
    path('login/',v1.login_view),
    path('group/',v1.groupview),
    path('reset/',v1.reset_password_view),
    path('accounts/profile/',v1.todo_create_view),
    path('createGroup/',v1.createGroupview),
    path('deleteGroups/',v1.deleteGroupsView),
    path('createtask/',v1.createtaskview),
    re_path(r'^groupAdmin/(?P<grpid>[\w\s]+)/$',v1.addAdminView),
    re_path(r'^attachTaskFile/(?P<id>[\d]+)/(?P<grpid>[\w\s]+)',v1.fileAttachmentView),
    re_path(r'^webLinkTask/(?P<id>[\d]+)/(?P<grpid>[\w\s]+)',v1.webLinkAttachmentView),
    re_path(r'^group/(?P<grpid>[\w\s]+)/$',v1.groupview),
    re_path(r'^group/(?P<grpid>[\w\s]+)/(?P<member>[\w\s]+)/$',v1.groupview),
    re_path(r'^mylist/(?P<mylist_choice>[\w-]+)/$',v1.mylist_view),
    re_path(r'^addmember/(?P<grpid>[\w\s]+)/$',v1.addMemberview),
    re_path(r'^addmember/(?P<grpid>[\w\s]+)/(?P<member>[\w\s]+)/$',v1.addMemberview),
    re_path(r'^createtask/(?P<grpid>[\w\s]+)/$',v1.createtaskview),
    re_path(r'^updateAssignedTask/(?P<id>[\d]+)/(?P<grpid>[\w\s]+)/$',v1.updateAssignedTaskView),
    re_path(r'^updateAssignedTask/(?P<id>[\d]+)/(?P<grpid>[\w\s]+)/(?P<activityOption>[\w-]+/$)',v1.updateAssignedTaskView),
    re_path(r'(?P<id>[\d]+)/description',v1.description_view),
    re_path(r'(?P<id>[\d]+)/summary',v1.summary_view),
    re_path(r'(?P<id>[\d]+)/detail',v1.task_detail_view),
    re_path(r'(?P<id>[\d]+)/update',v1.updatelist_view),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
	
