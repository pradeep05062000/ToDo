from django.shortcuts import render,redirect
from todoapp.forms import SignUpForm,ResetPasswordForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from todoapp.models import ToDoModel,SummaryModel,GroupModel,TaskAssignModel
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime,time
from django.http import Http404
from todoapp.supporting_python import task_detail_modifed,task_flag_update
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.

######################Sign Up page function###########################################################

def signup_view(request):
    form=SignUpForm()                            #####creating the object of SignUpForm class

    if request.method=='POST':
        form=SignUpForm(request.POST)            #####'request.POST' contain the data passed by signup form through post request
        if form.is_valid():                      #####'is_valid()' function checks all the fields contains the valid info or not it also check for validators set for particular fields
            user=form.save()                     #############this saves the data in database
            user.set_password(user.password)     #######'set_password' method converts the raw password in to hashed password(encrypted) 'user.password' this contains the raw password
            user.save()                          #############this saves the data in database
            return HttpResponseRedirect('/accounts/login')          ######here we redirect path '/accounts/login' url

    return render(request,'todoapp/signup.html',{'form':form})   ########### 'render()'  function insert the context inside template('signup.html')
############################################################################################################
@login_required            
def mylist_view(request,mylist_choice):
    data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)

    if request.method=='POST':                              #######
        for x in request.POST:                              #   This logic is used to select and delete the multipul objects
            if x.isnumeric():                               #
                ToDoModel.objects.get(id=x).delete()        #######

    if mylist_choice == 'mylist':
        alldata=ToDoModel.objects.filter(user=request.user)
        return render(request,'todoapp/mylist.html',{'data':data,'alldata':alldata,'current_user':request.user})

    elif mylist_choice=='todo':
        data_todo=ToDoModel.objects.filter(user=request.user,status='todo')
        return render(request,'todoapp/mylist.html',{'data':data,'alldata':data_todo,'current_user':request.user,'todo':True})

    elif mylist_choice == 'inProgress':
        data_inprogress = ToDoModel.objects.filter(user=request.user,status='inProgress')
        return render(request,'todoapp/mylist.html',{'data':data,'alldata':data_inprogress,'current_user':request.user,'inProgress':True})

    elif mylist_choice == 'done':
        data_done = ToDoModel.objects.filter(user=request.user,status='done')
        return render(request,'todoapp/mylist.html',{'data':data,'alldata':data_done,'current_user':request.user,'done':True})
    
##############################################################################################################################


##############################################################################################################################
@login_required
def reset_password_view(request):

    
    if request.method == "POST":
        form=ResetPasswordForm(request.POST,request=request)        ########## Request is sent to constructor of ResetPasswordForm Class
        if form.is_valid():
            try:
                userN=User.objects.get(username=request.user)
                userN.set_password(form.cleaned_data['newp'])       ########## Raw Password is converted into hassing(encrypted) using set_password function
                userN.save()
                messages.success(request, 'Password Changed Succesfully')
            except:
                messages.success(request, 'Username DoesNotExist')

    else:
        form=ResetPasswordForm

    data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/reset_password.html',{'form':form,'current_user':request.user,'data':data})   

##########################################################################################################################################

@login_required                 #################################login_required is the decorater use to restrict the user to go in that page before authenticating itself .
def todo_create_view(request):
    
    error = True
    if request.method=='POST':
            mylist_data=ToDoModel()  
            mylist_data.task=request.POST.get('task') 
            mylist_data.date=datetime(int(request.POST.get('year')),int(request.POST.get('month')),int(request.POST.get('day'))).date()
            mylist_data.time=time(int(request.POST.get('hour')),int(request.POST.get('min')))
            mylist_data.description=request.POST.get('description') 
            mylist_data.flagTask = "no"
            mylist_data.user=request.user
            mylist_data.save() 

            summary=SummaryModel()  
            summary.taskId=mylist_data          ##################### Here we assigne the ToDoModel object id to taskId of SummaryModel
            summary.dateTime=datetime.now()
            summary.description_summary=request.POST.get('description')
            summary.modefied_detail="created at {} {}".format(datetime.now().strftime("%b %d, %Y"),datetime.now().strftime("%I:%M %p").lower()) 
            summary.created_update="created"
            summary.save()    

            return redirect('/mylist/mylist')

    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/todo_create.html',{'current_user':request.user,'data':mylist_data})


#############################This function is used to update the the task #####################################

def updatelist_view(request,id):
    error=False
    if request.method=='POST':
        mylist_data=ToDoModel.objects.get(id=id)
        summary=SummaryModel() 
        modefied_dt,flag = task_detail_modifed(request.POST.get('description'),request.POST.get('status'), 
                datetime(int(request.POST.get('year')),int(request.POST.get('month')),int(request.POST.get('day'))).date(),
                time(int(request.POST.get('hour')),int(request.POST.get('min'))),id)
        
        if modefied_dt != False :
            if flag[0] == "True":
                mylist_data.date=datetime(int(request.POST.get('year')),int(request.POST.get('month')),int(request.POST.get('day'))).date()
            if flag[1] == "True":
                mylist_data.time=time(int(request.POST.get('hour')),int(request.POST.get('min')))
            if flag[2] == "True":
                mylist_data.status=request.POST.get('status')
            if flag[3] == "True":
                mylist_data.description=request.POST.get('description')
            mylist_data.user=request.user  
            mylist_data.flagTask = "no"       
            mylist_data.save()

            summary.taskId=mylist_data
            summary.dateTime=datetime.now()
            if flag[3] == "True":
                summary.description_summary=request.POST.get('description') 
            summary.modefied_detail=modefied_dt 
            summary.created_update="updated"
            summary.save() 
            messages.success(request, 'Task Updated Successfully')
                
        else:
            updated = None
            messages.info(request, 'No changes detected while updating task') 
        

    data=ToDoModel.objects.get(id=id)
    date_lst=str(data.date).split('-')
    time_lst=str(data.time).split(':')
    mylist_data =ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/update.html',{'current_user':request.user,"status":data.status,'description':data.description,'task':data.task,
        'day':int(date_lst[2]),'month':date_lst[1],'year':int(date_lst[0]),'hour':time_lst[0],'min':time_lst[1]}) 


##################This three function are used to show log of task in short/detail#########################################################################
    
def description_view(request,id):
    data=ToDoModel.objects.get(id=id)
    description_data=SummaryModel.objects.filter(taskId=id)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/description.html',{"description_data":description_data,'id':id,'description':data.description,
        'current_user':request.user,'task':data.task,'time':data.time,'date':data.date,'data':mylist_data}) 

def summary_view(request,id):
    data=ToDoModel.objects.get(id=id)
    summary_data=SummaryModel.objects.filter(taskId=id)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/summary.html',{'summary_data':summary_data,'current_user':request.user,'data':mylist_data,'task':data.task,'id':id})

def task_detail_view(request,id):
    data=ToDoModel.objects.get(id=id)
    detail_data=SummaryModel.objects.filter(taskId=id)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/task_detail.html',{'detail_data':detail_data,'current_user':request.user,'data':mylist_data,'task':data.task,})
    

####################This function is used to create group#########################################################################

def groupview(request):

   
    if request.method == 'POST':
        flag = False
        addGrp = GroupModel()
        allGroupData = GroupModel.objects.all()
        for data in allGroupData:
            if data.created_by == str(request.user) and data.group == request.POST.get('group'):
                flag = True

        if flag == False:
            addGrp.member = request.user
            addGrp.created_by = str(request.user) 
            addGrp.group = request.POST.get('group')
            addGrp.save()

        else:
            messages.info(request, 'You have already created group')

        

    grpdata_member=GroupModel.objects.filter(member=request.user)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)


    return render(request,'todoapp/creategroup.html',{'current_user':request.user,'grpdata_member':grpdata_member,'data':mylist_data})

#####################################This function is used to add members in group#############################3
def addMemberview(request,created_by=None,group=None,member=None):
    flag,memberFlag,addmemberFlag = False,True,False


    if created_by == str(request.user) :
        addmemberFlag = True

    if member != None:
        allGroupData = GroupModel.objects.all()
        for grpData in allGroupData:
            if grpData.created_by == created_by and grpData.group == group and str(grpData.member) == member:
                flag = True
            
        
        if flag == False:
                userData = User.objects.all()       
                addMember = GroupModel()
                addMember.created_by = created_by
                addMember.group = group
                for x in userData:
                    if str(x.username) == member:
                        addMember.member = x
                        addMember.save()
                        memberFlag = False
                        break
                if memberFlag:
                    messages.info(request, 'No such username')
        else:
            messages.info(request, 'Member already exist')


    grp_member = GroupModel.objects.filter(created_by=created_by,group=group)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)


    return render(request, 'todoapp/addmember.html',{'current_user':request.user,'created_by':created_by,
        'group':group,'grp_member':grp_member,'data':mylist_data,'addmemberFlag':addmemberFlag})

        
###########################Function is used to show Task Assigned to members###################################
def taskAssignedview(request,id):

    taskassigned = TaskAssignModel.objects.filter(assigned_to=id)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)

    return render(request,'todoapp/taskassigned.html',{'current_user':request.user,'taskassigned':taskassigned,'data':mylist_data})

######################This function is used to assign tasks to members######################################################
def createtaskview(request,created_by,group):


    if request.method == 'POST':
        memberObject = GroupModel.objects.get(id=request.POST.get('member_id'))
        task_assign = TaskAssignModel()
        task_assign.assigned_to = memberObject
        task_assign.task = request.POST.get('task')
        task_assign.assigned_by = str(request.user)
        task_assign.save()
        messages.success(request, 'Task Assigned Successfully')


    grp_member = GroupModel.objects.filter(created_by=created_by,group=group)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)


    return render(request,'todoapp/createtask.html',{'current_user':request.user,'grp_member':grp_member,'data':mylist_data})

#######################################################################################################################################







