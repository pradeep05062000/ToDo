from django.shortcuts import render,redirect
from todoapp.forms import SignUpForm,ResetPasswordForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from todoapp.models import ToDoModel,SummaryModel,GroupModel,TaskAssignModel,GroupTaskActivityModel
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime,time
from django.http import Http404
from todoapp.supporting_python import task_detail_modifed,task_flag_update,activityCheck,verifyGroupAdmin
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse


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
@login_required
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
    date_listAllMemberTask=str(data.date).split('-')
    time_listAllMemberTask=str(data.time).split(':')
    mylist_data =ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/update.html',
        {'current_user':request.user,"status":data.status,'description':data.description,'task':data.task,'day':int(date_listAllMemberTask[2]),
        'month':date_listAllMemberTask[1],'year':int(date_listAllMemberTask[0]),'hour':time_listAllMemberTask[0],'min':time_listAllMemberTask[1]}) 


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
@login_required
def groupview(request,grpid=None,member=None):

    listAllMemberTaskFlag,singleMemberTasksFlag = False,False
    grpdata_member=GroupModel.objects.filter(member=request.user)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)

    if grpid == None:
        listAllMemberTask = []
        grpdata = GroupModel.objects.filter(member=request.user)
        for x in grpdata:
            grpid = x.grpid
            break
        selectedGroups=GroupModel.objects.filter(grpid=grpid)
        for x in selectedGroups:
            listAllMemberTask.append(TaskAssignModel.objects.filter(assigned_to_id=x.id))

        for x in listAllMemberTask:
            if len(x) != 0:
                listAllMemberTaskFlag = True
        return render(request,'todoapp/creategroup.html',
            {'listAllMemberTaskFlag':listAllMemberTaskFlag,'selectedGroups':selectedGroups,'current_user':request.user,
            'grpid':grpid ,'grpdata_member':grpdata_member,'data':mylist_data,'listAllMemberTask':listAllMemberTask})

    elif member == None:
        listAllMemberTask = []
        selectedGroups=GroupModel.objects.filter(grpid=grpid)
        for x in selectedGroups:
            listAllMemberTask.append(TaskAssignModel.objects.filter(assigned_to_id=x.id))

        for x in listAllMemberTask:
            if len(x) != 0:
                listAllMemberTaskFlag = True
        return render(request,'todoapp/creategroup.html',
            {'listAllMemberTaskFlag':listAllMemberTaskFlag,'selectedGroups':selectedGroups,'current_user':request.user,
            'grpid':grpid,'grpdata_member':grpdata_member,'data':mylist_data,'listAllMemberTask':listAllMemberTask})
    else:
        singleMemberTasks = []
        selectedGroups=GroupModel.objects.filter(grpid=grpid)
        userData = User.objects.all() 
        for x in userData:
            if str(x.username) == member:
                singleGroup=GroupModel.objects.filter(grpid=grpid,member=x)
                break

        for x in singleGroup:
            singleMemberTasks.append(TaskAssignModel.objects.filter(assigned_to_id=x.id))

        for x in singleMemberTasks:
            if len(x) != 0:
                singleMemberTasksFlag = True
                break

        return render(request,'todoapp/group.html',
            {'singleMemberTasksFlag':singleMemberTasksFlag,'selectedGroups':selectedGroups,'current_user':request.user,'member':member,'grpid':grpid,
            'grpdata_member':grpdata_member,'data':mylist_data,'singleMemberTasks':singleMemberTasks})
    

        
###################################################################################################################################
@login_required
def createGroupview(request):

    listAllMemberTaskFlag = False
    verifyUserFlag = verifyGroupAdmin(str(request.user))

    if request.method == 'POST':
        if len(request.POST.get('group')) >= 2:
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
                gid = GroupModel.objects.get(id=addGrp.id)
                gid.grpid = str(gid.id) + gid.group[0:2]
                gid.save()
                messages.success(request, 'Group created Successfully')
            else:
                messages.info(request, 'You have already created group')


        else:
            messages.info(request, 'Group name must contain atleast 2 characters')


        listAllMemberTask = []
        grpdata = GroupModel.objects.filter(member=request.user)
        for x in grpdata:
            grpid = x.grpid
            break
        selectedGroups=GroupModel.objects.filter(grpid=grpid)
        for x in selectedGroups:
            listAllMemberTask.append(TaskAssignModel.objects.filter(assigned_to_id=x.id))

        for x in listAllMemberTask:
            if len(x) != 0:
                listAllMemberTaskFlag = True
        
        grpdata_member=GroupModel.objects.filter(member=request.user)
        mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
        task_flag_update(request.user)

        return render(request,'todoapp/creategroup.html',
            {'listAllMemberTaskFlag':listAllMemberTaskFlag,'selectedGroups':selectedGroups,'current_user':request.user,'verifyUserFlag':verifyUserFlag,
            'grpid':grpid ,'grpdata_member':grpdata_member,'data':mylist_data,'listAllMemberTask':listAllMemberTask})


#####################################This function is used to add members in group#############################
@login_required
def addMemberview(request,grpid=None,member=None):
    flag,memberFlag = False,True



    if member != None:

        allGroupData = GroupModel.objects.filter(grpid=grpid)
        for grpData in allGroupData:
            if grpid == grpid and str(grpData.member) == member:
                flag = True
            
        
        if flag == False:
                userData = User.objects.all()   
                grpAddMember = GroupModel.objects.filter(grpid=grpid) 
                for x in grpAddMember:
                    created_by = x.created_by
                    group = x.group
                    break

                addMember = GroupModel()
                addMember.grpid = grpid
                addMember.created_by = created_by
                addMember.group = group
                for x in userData:
                    if str(x.username) == member:
                        addMember.member = x
                        addMember.save()
                        memberFlag = False
                        messages.info(request, 'Username Added')
                        break
                if memberFlag:
                    messages.info(request, 'No such username')
        else:
            messages.info(request, 'Member already exist')


    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)


    return render(request, 'todoapp/addmember.html',
        {'current_user':request.user,'grpid':grpid,'data':mylist_data})

        
###########################Function is used to show Task Assigned to members###################################
def taskAssignedview(request,id):

    taskassigned = TaskAssignModel.objects.filter(assigned_to_id=id)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)

    return render(request,'todoapp/taskassigned.html',{'current_user':request.user,'taskassigned':taskassigned,'data':mylist_data})

######################This function is used to assign tasks to members######################################################
@login_required
def createtaskview(request,grpid):


    if request.method == 'POST':
        memberObject = GroupModel.objects.get(id=request.POST.get('member_id'))
        task_assign = TaskAssignModel()
        task_assign.assigned_to_id = memberObject
        task_assign.assigned_to_name = memberObject.member
        task_assign.task = request.POST.get('task')
        task_assign.status = 'todo'
        task_assign.comment = request.POST.get('comment')
        task_assign.assigned_by = str(request.user)
        task_assign.save()
        messages.success(request, 'Task Assigned Successfully')

        activityDetail = GroupTaskActivityModel()
        activityDetail.grpTaskActivity_id = task_assign
        activityDetail.activity = 'Task:  ' +request.POST.get('task') +'\n' "Status:  " + "ToDo\n" + "Comment:  " + request.POST.get('comment') +'\n' + 'Assigned To:  ' + str(memberObject.member)
        activityDetail.dateTime = datetime.now()
        activityDetail.updated_by = str(request.user)
        activityDetail.save()


    grp_member = GroupModel.objects.filter(grpid=grpid)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)


    return render(request,'todoapp/createtask.html',{'current_user':request.user,'grp_member':grp_member,'data':mylist_data})

#######################################################################################################################################
@login_required
def updateAssignedTaskView(request,id,grpid):

    updateTask = TaskAssignModel.objects.get(id=id)
    
    if request.method == 'POST':
        activityCheckFlag,flag = activityCheck(request.POST.get('comment'),request.POST.get('task'),request.POST.get('status'),
            request.POST.get('member_id'),id)
        updateTask = TaskAssignModel.objects.get(id=id)
        memberObject = GroupModel.objects.get(id=request.POST.get('member_id'))
        updateTask.assigned_to_id = memberObject
        updateTask.assigned_to_name = str(memberObject.member)
        updateTask.task = request.POST.get('task')
        updateTask.status = request.POST.get('status')
        updateTask.comment = request.POST.get('comment')
        updateTask.assigned_by = str(request.user)
        updateTask.save()

        if activityCheckFlag != False :
            activityDetail = GroupTaskActivityModel()                
            activityDetail.grpTaskActivity_id = updateTask
            activityDetail.activity = activityCheckFlag
            activityDetail.dateTime = datetime.now()
            activityDetail.updated_by = str(request.user)
            activityDetail.save()

    task = updateTask.task
    assigned_to_id = updateTask.assigned_to_id_id
    assigned_to_name = updateTask.assigned_to_name
    status = updateTask.status
    comment = updateTask.comment
    assigned_by = updateTask.assigned_by

    grp_member = GroupModel.objects.filter(grpid=grpid)
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)

    delailedActivity = GroupTaskActivityModel.objects.filter(grpTaskActivity_id_id=id)


    return render(request,'todoapp/updateAssignedTask.html',
        {'status':status,'current_user':request.user,'task':task,'grp_member':grp_member,'comment':comment,'delailedActivity':delailedActivity,
        'assigned_to_id':assigned_to_id,'assigned_by':assigned_by,'assigned_to_name':assigned_to_name,'data':mylist_data})





