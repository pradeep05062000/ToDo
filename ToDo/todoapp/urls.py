

from django.urls import path,re_path
from todoapp import views as v1            

urlpatterns = [
    path('',v1.todo_create_view),
    path('signup/',v1.signup_view),
    re_path(r'^mylist/(?P<mylist_choice>[\w-]+)/$',v1.mylist_view),
    path('reset/',v1.reset_password_view),
    path('<id>/discription',v1.discription_view),
    path('<id>/summary',v1.summary_view),
    path('<id>/detail',v1.task_detail_view),
    path('<id>/update',v1.updatelist_view),
    path('accounts/profile/',v1.todo_create_view),
]
	
