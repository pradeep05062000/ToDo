

from django.urls import path,re_path
from todoapp import views as v1            

urlpatterns = [
    path('',v1.todo_create_view),
    path('signup/',v1.signup_view),
    path('group/',v1.groupview),
    path('reset/',v1.reset_password_view),
    path('accounts/profile/',v1.todo_create_view),
    re_path(r'^mylist/(?P<mylist_choice>[\w-]+)/$',v1.mylist_view),
    re_path(r'^addmember/(?P<created_by>[\w-]+)/(?P<group>[\w\s]+)/$',v1.addMemberview),
    re_path(r'^addmember/(?P<created_by>[\w-]+)/(?P<group>[\w\s]+)/((?P<member>[\w\s]+)|($))/$',v1.addMemberview),
    re_path(r'^taskassigned/(?P<id>[\d]+)/$',v1.taskAssignedview),
    re_path(r'^createtask/(?P<created_by>[\w-]+)/(?P<group>[\w\s]+)/$',v1.createtaskview),
    re_path(r'(?P<id>[\d]+)/description',v1.description_view),
    re_path(r'(?P<id>[\d]+)/summary',v1.summary_view),
    re_path(r'(?P<id>[\d]+)/detail',v1.task_detail_view),
    re_path(r'(?P<id>[\d]+)/update',v1.updatelist_view),
]
	
