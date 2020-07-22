from django.shortcuts import render,redirect
from todoapp.forms import SignUpForm,ResetPasswordForm,GroupTaskAttachmentsForm,GroupTaskWebLinkForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from todoapp.models import ToDoModel,SummaryModel,GroupModel,TaskAssignModel,GroupTaskActivityModel,GroupAdminsModel,GroupTaskAttachmentsModel,GroupTaskWebLinkModel
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime,time
from django.http import Http404
from todoapp.supporting_python import task_detail_modifed,task_flag_update,historyCheck,verifyGroupAdmin
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse
from django.core.mail import send_mail

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
##'mylist_choice' parameter was added to know which page has been selected by end user from 'mylist','todo','inProgress','done'

    data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)

    if request.method=='POST':                              #######
        for x in request.POST:                              #   This logic is used to select and delete the multipul objects
            if x.isnumeric():                               #
                ToDoModel.objects.get(id=x).delete()        #######

    if mylist_choice == 'mylist':
        alldata=ToDoModel.objects.filter(user=request.user)
        return render(request,'todoapp/mylist.html',{'data':data,'alldata':alldata,'current_user':request.user})
        ##'data' parameter is used to send the data for task notification 
        ##'alldata' parameter used to send all task of end user and same for 'todo','in progress' and 'done' tasks

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
        form=ResetPasswordForm(request.POST,request=request)       
         ########## Request is sent to constructor of ResetPasswordForm Class to check how is current user
         #### request.POST is dict type parameter used to send all data of reset password form

        if form.is_valid():
            try:
                userN=User.objects.get(username=request.user)
                userN.set_password(form.cleaned_data['newp'])       
                ########## Raw Password is converted into hassing(encrypted) using set_password function

                userN.save()
                messages.success(request, 'Password Changed Succesfully')
            except:
                messages.success(request, 'Username DoesNotExist')

    else:
        form=ResetPasswordForm

    data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    return render(request,'todoapp/reset_password.html',{'form':form,'current_user':request.user,'data':data})   

#######################Following view is used to create the personal tasks ###############################################

@login_required                 #################################login_required is the decorater use to restrict the user to go in that page before authenticating itself .
def todo_create_view(request):
    
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
    #error=False
    if request.method=='POST':
        mylist_data=ToDoModel.objects.get(id=id)
        summary=SummaryModel() 
        modefied_dt,flag = task_detail_modifed(request.POST.get('description'),request.POST.get('status'), 
                datetime(int(request.POST.get('year')),int(request.POST.get('month')),int(request.POST.get('day'))).date(),
                time(int(request.POST.get('hour')),int(request.POST.get('min'))),id)
        ##This task_detail_modifed function is used to check values are same or changed of the variables 
        if modefied_dt != False :
            if flag[0] == "True":
                mylist_data.date=datetime(int(request.POST.get('year')),int(request.POST.get('month')),int(request.POST.get('day'))).date()
            if flag[1] == "True":
                mylist_data.time=time(int(request.POST.get('hour')),int(request.POST.get('min')))
            if flag[2] == "True":
                mylist_data.status=request.POST.get('status')
            if flag[3] == "True":
                mylist_data.description=request.POST.get('description')
            ##This four if condition are set too check anything updated or not, if not it don't update in model

            mylist_data.user=request.user  
            mylist_data.flagTask = "no"       
            mylist_data.save()

            summary.taskId=mylist_data
            ##### Here the taskId is foreign key and we are assigning object of TodoModel to taskId 
            ##### due to which summary object get linked to TodoModel

            summary.dateTime=datetime.now()
            if flag[3] == "True": ## if is used to check any update in description
                summary.description_summary=request.POST.get('description') 
            summary.modefied_detail=modefied_dt 
            summary.created_update="updated"
            summary.save() 
            messages.success(request, 'Task Updated Successfully')
                
        else:
            #updated = None
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
    ##Here we are retreiving all the SummaryModel objects related to seleted task
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
    

####################This function is used to Show the group details#########################################################################
@login_required
def groupview(request,grpid=None,member=None):

    listAllMemberTaskFlag,singleMemberTasksFlag = False,False 
    ### this flags are used to check where all members from group are selected or single member
    grpAdmins = GroupAdminsModel.objects.all()
    ## Here we are retrieving all adminss

    grpdata_member=GroupModel.objects.filter(member=request.user)
    ##Here we are retreivng groups related to current end user
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    verifyUserFlag = verifyGroupAdmin(str(request.user))
    grpdata = GroupModel.objects.filter(member=request.user)
    ## We are retriving all the group associated with the current user
           


    if len(grpdata) != 0:
        if grpid == None: #### grip == None means no group has been seleted by end user
            listAllMemberTask = []
            for x in grpdata:
                grpid = x.grpid
                ###This step tell us first group has been selected 
                ##because to show all data of the first group by default, when user enters to group view
                break
            selectedGroups=GroupModel.objects.filter(grpid=grpid)
            ##Know Using grpid we retrive all the same groups from GroupModel (which means we get all the users of that group)
            for x in selectedGroups:
                listAllMemberTask.append(TaskAssignModel.objects.filter(assigned_to_id=x.id))
                ##Here we are adding all members task object in the list
                ##We do so, because each member can have multiple task and task all task are grouped in single index of list
                ## Because we cannot send all tasks, of all member without using list

            for x in listAllMemberTask:
                if len(x) != 0:
                    listAllMemberTaskFlag = True
                    ##Here we are check is listAllMemberTask is empty or not
                    ##Because if it is empty than listAllMemberTaskFlag remains False and which indicates there are no task for any user in that group

            return render(request,'todoapp/group.html',
                {'listAllMemberTaskFlag':listAllMemberTaskFlag,'selectedGroups':selectedGroups,'current_user':request.user,'verifyUserFlag':verifyUserFlag,
                'grpid':grpid ,'grpdata_member':grpdata_member,'data':mylist_data,'listAllMemberTask':listAllMemberTask,'grpAdmins':grpAdmins})

        elif member == None: ##In this conditon group is selected by user and we required to show all data of that grp
            listAllMemberTask = []
            selectedGroups=GroupModel.objects.filter(grpid=grpid)
            for x in selectedGroups:
                listAllMemberTask.append(TaskAssignModel.objects.filter(assigned_to_id=x.id))

            for x in listAllMemberTask:
                if len(x) != 0:
                    listAllMemberTaskFlag = True
            return render(request,'todoapp/group.html',
                {'listAllMemberTaskFlag':listAllMemberTaskFlag,'selectedGroups':selectedGroups,'current_user':request.user,'verifyUserFlag':verifyUserFlag,
                'grpid':grpid,'grpdata_member':grpdata_member,'data':mylist_data,'listAllMemberTask':listAllMemberTask,'grpAdmins':grpAdmins})

        else:##In this condition we are selecting the data of single user 
            singleMemberTasks = []
            selectedGroups=GroupModel.objects.filter(grpid=grpid)
            userData = User.objects.all() 
            for x in userData:
                if x.username == member:
                    singleGroup=GroupModel.objects.filter(grpid=grpid,member=x)
                    break

            for x in singleGroup:
                singleMemberTasks.append(TaskAssignModel.objects.filter(assigned_to_id=x.id))

            for x in singleMemberTasks:
                if len(x) != 0:
                    singleMemberTasksFlag = True
                    break

            return render(request,'todoapp/group.html',
                {'singleMemberTasksFlag':singleMemberTasksFlag,'selectedGroups':selectedGroups,'current_user':request.user,'member':member,'grpid':grpid,'verifyUserFlag':verifyUserFlag,
                'grpdata_member':grpdata_member,'data':mylist_data,'singleMemberTasks':singleMemberTasks,'grpAdmins':grpAdmins})
    
    else:
        return render(request,'todoapp/group.html',
            {'noGroups':'True','current_user':request.user,'verifyUserFlag':verifyUserFlag,'data':mylist_data,'grpAdmins':grpAdmins})

        
###################################################################################################################################
@login_required
def createGroupview(request):

    if request.method == 'POST':
        if len(request.POST.get('group')) >= 2:  ##This conditon is used coz, if length is small, then  while creating grpid by using slicing we will get an error
            flag = False
            addGrp = GroupModel()
            allGroupData = GroupModel.objects.all()
            for data in allGroupData:
                if data.group == request.POST.get('group'):
                    flag = True
                    ##Here we are checking do group already exist or not, if yes flag will be True.

            if flag == False:
                addGrp.member = request.user # here member is foregin key and we are adding first member of group as current user by default
                addGrp.created_by = str(request.user) 
                addGrp.group = request.POST.get('group')
                addGrp.save()
                gid = GroupModel.objects.get(id=addGrp.id) 
                ##Here we are creating new object of same recently created group object
                ##Because we require id of recently created group to create grpid of same group and we will not get group id untill we dont save that group object
                gid.grpid = str(gid.id) + gid.group[0:2]
                gid.save()
                mail_subject = "Your were added in " + "'" + request.POST.get("group") + "'" + ' by ' +str(request.user)
                userAddMail = User.objects.get(username = request.user)
                send_mail('New Group Created',mail_subject,'djangoemail2020@gmail.com' , [userAddMail.email] , fail_silently=False)
                messages.success(request, 'Group created Successfully')
            else:
                messages.info(request, 'Group already exist')


        else:
            messages.info(request, 'Group name must contain atleast 2 characters')


        
    grpdata_member=GroupModel.objects.filter(member=request.user)
    ##Here we are retrieving all the groups of current loged in user
    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)
    
    return render(request,'todoapp/createGroup.html',
            {'current_user':request.user ,'grpdata_member':grpdata_member,'data':mylist_data})

########################################################################################################################
import re
def deleteGroupsView(request):

    if request.method == 'POST':
        for x in request.POST:
            if re.search("group==",x): ## This condition is used to check match of "group==" with the string
                lst = x.split('==') ###Here we split the string too extract the actual grpid
                if request.POST[x] == 'on':
                    deletingGrp = GroupModel.objects.filter(grpid=lst[1])
                    for data in deletingGrp: ## By using loop we delete all GroupModel objects which contain same grpid
                        deleteGrp_mail = User.objects.get(username=data.member)
                        mail_subject = "'"+ data.group +"'" + ' group deleted by ' + str(request.user)
                        send_mail('Group Deleted',mail_subject,'djangoemail2020@gmail.com' , [deleteGrp_mail.email] , fail_silently=False)                         
                        GroupModel.objects.get(id=data.id).delete()

    return redirect('/createGroup/')


#####################################This function is used to add members in group#############################
@login_required
def addMemberview(request,grpid=None,member=None):
    flag,memberFlag = False,True

    if request.method == 'POST':
        for x in request.POST:
            if x.isnumeric():
                groupMemeber = GroupModel.objects.get(id=x)
                GroupModel.objects.get(id=x).delete()
                deleteUser = User.objects.all()
                for x in deleteUser:
                    if x.username == str(groupMemeber.member):
                        mail_subject = 'You were removed from group ' + groupMemeber.group + '\nRemoved by ' + str(request.user) 
                        send_mail('Removed From Group',mail_subject,'djangoemail2020@gmail.com' , [x.email] , fail_silently=False)
                        messages.info(request, 'Deleted Successfully')



    if member != None:
        ##This condition is written to check wether input field of username is empty or not
        ##If it is empty and user just click add button then due to this condition, no member will be added

        allGroupData = GroupModel.objects.filter(grpid=grpid)
        ##Here we are retrieving all objects from the GroupModels (all member of grpid group)
        for grpData in allGroupData:
            if grpid == grpid and str(grpData.member) == member:
                flag = True
                #At this step we are checking if user all ready exist or not , if yes flag will go True.
            
        
        if flag == False:
                userData = User.objects.all()   
                grpAddMember = GroupModel.objects.filter(grpid=grpid)


                for x in grpAddMember: 
                    created_by = x.created_by
                    group = x.group
                    break
                    #This step is use to retrieve group and created_by variable value to assign, new member object.

                addMember = GroupModel()
                addMember.grpid = grpid
                addMember.created_by = created_by
                addMember.group = group
                for x in userData:
                    if x.username == member:
                        #This step verification is done , because we don't know which object in  user data contains the provided user name
                        #And if we dont find the provide user name memberFlag will remain True, which means know such user exist.

                        addMember.member = x
                        # Here the member is foregin key connected to User model
                        #And in the above step we are assigning the User's model object to member variable, which contains the provided username by end user.
                        addMember.save()
                        memberFlag = False
                        mail_subject = 'You were added in new group by ' + str(request.user) +'\n GroupName: ' + group 
                        send_mail('New Group',mail_subject,'djangoemail2020@gmail.com' , [x.email] , fail_silently=False)
                        messages.info(request, 'Username Added')
                        break
                if memberFlag:
                    messages.info(request, 'No such username')
        else:
            messages.info(request, 'Member already exist')


    return redirect('/group/' + grpid)
    
###################################################################################################################################
@login_required
def addAdminView(request,grpid=None):
    userExistFlag,userNotExistFlag = False,True

    if request.method == 'POST':
        grpAdmins = GroupAdminsModel.objects.all() #In this step we are retrieving all objects from Admin Model
        for x in request.POST:                              #   This logic is used to select and delete the Admin objects
            if x.isnumeric():  
                admin_user = GroupAdminsModel.objects.get(id=x)
                deleteUser = User.objects.get(id=admin_user.adminUser_id_id)  
                GroupAdminsModel.objects.get(id=x).delete()
                mail_subject = 'You are no longer admin \n Removed by ' + str(request.user)
                send_mail('Group Admin',mail_subject,'djangoemail2020@gmail.com' , [deleteUser.email] , fail_silently=False)                         
                

        allUserObject = User.objects.all()

        for x in allUserObject:
            if x.username == request.POST.get('admin'):
                userObject = User.objects.get(username=x.username)
                userNotExistFlag = False
                #Here using for loop and if condition we are checking do provided username by end user exist or not in User Model
                break;

        for x in grpAdmins:
            if x.adminUser == request.POST.get('admin'):
                userExistFlag = True
                messages.info(request, 'Username already exists')
                # In this step we are check admin user already exist or not in Admin Model
                break;


        if userNotExistFlag == False and userExistFlag == False:
            ##Here we check that, if user exist in User Model and user already does not exists in Admin Model
            ##And if above condition is True we add user in Admin model, by using steps below.
            adminObject = GroupAdminsModel()
            adminObject.adminUser_id = userObject
            adminObject.adminUser = request.POST.get('admin')
            adminObject.save()
            mail_subject = 'You have got admin rights\n' + 'You were added by ' + str(request.user)
            send_mail('Group Admin',mail_subject,'djangoemail2020@gmail.com' , [userObject.email] , fail_silently=False)


        if request.POST.get('admin'):
            #This condition is used, because if we delete any user then that is also an post request 
            #And it does not contain the admin. Due to this condition interpreter does not enter inside
            #And this will avoid from showing following message('No such Username') to end user, when any admin is deleted.
            if userNotExistFlag == True:
                messages.info(request, 'No such username')

    return redirect('/group/' + grpid)

 
######################This function is used to assign tasks to members######################################################
@login_required
def createtaskview(request,grpid=None):


    if request.method == 'POST':
        memberObject = GroupModel.objects.get(id=request.POST.get('member_id')) 
        #This member_id variable of post request contains id of Group Model object, to whom we are assiging task
        task_assign = TaskAssignModel()
        task_assign.assigned_to_id = memberObject
        #Here the assigned_to_id is foreign key connected to Group Model
        #And we are assigning object of Group model (to whom we are going to assign task) to assigned_to_id

        task_assign.assigned_to_name = str(memberObject.member)
        task_assign.task = request.POST.get('task')
        task_assign.status = 'ToDo'
        task_assign.comment = request.POST.get('comment')
        task_assign.assigned_by = str(request.user)
        task_assign.save()
        mail_subject ='You have got new task by ' + str(request.user) + '\nTask Name :-' + request.POST.get('task')
        send_email_to = User.objects.get(username = memberObject.member)
        send_mail('New Task Assigned',mail_subject,'djangoemail2020@gmail.com' , [send_email_to.email] , fail_silently=False)
        
        messages.success(request, 'Task Assigned Successfully')
        historyDetail = GroupTaskActivityModel()
        historyDetail.grpTaskActivity_id = task_assign
        #Here the grpTaskActivity_id is foreign key connected to TaskAssignModel
        #And we are assiging the object of TaskAssign Model (which contains the member to whom we recently assigend task above)
        historyDetail.comments = request.POST.get('comment')
        historyDetail.history = 'Task:  ' +request.POST.get('task') +'\n' "Status:  " + "ToDo\n" + "Comment:  " + request.POST.get('comment') +'\n' + 'Assigned To:  ' + str(memberObject.member)
        historyDetail.dateTime = datetime.now()
        historyDetail.updated_by = str(request.user)
        historyDetail.save()

    return redirect('/group/'+ grpid )

#######################################################################################################################################
@login_required
def updateAssignedTaskView(request,id=None,grpid=None,activityOption=None):
    historyFlag = False
    updateTask = TaskAssignModel.objects.get(id=id)
    #This is object which we are going to update in steps below
    allfiles = GroupTaskAttachmentsModel.objects.filter(fileTask_id=id)
    #Here we are retrieving all the files attached with this  object (updateTask)
    #The fileTask_id is the foreign key connected to TaskAssigenModel
    allLinks = GroupTaskWebLinkModel.objects.filter(linkTask_id=id)
    #Same for all the link attach to task
    grp_member = GroupModel.objects.filter(grpid=grpid)
    #Here we are retreiving all the member of the group 
    #Because this member are required when we want to update assigen_to field
    for x in grp_member:
        groupName = x.group
        break
    formFile = GroupTaskAttachmentsForm()
    formLink = GroupTaskWebLinkForm()
    if activityOption == 'History/':
        historyFlag = True 
        ##At this step we are checking History button is click or not by end user
    
    if request.method == 'POST':
        historyCheckFlag,flag = historyCheck(request.POST.get('comment'),request.POST.get('task'),request.POST.get('status'),
            request.POST.get('member_id'),id)
        ##By using historyCheck function defined in supportin_python file
        ##we check which fields are updated by end user while updating task
        updateTask = TaskAssignModel.objects.get(id=id)
        #Here we are retreivng object of TaskAssignModel (To which we are updating)
        if request.POST.get('member_id'):
            memberObject = GroupModel.objects.get(id=request.POST.get('member_id'))
            updateTask.assigned_to_id = memberObject
            updateTask.assigned_to_name = str(memberObject.member)
        if request.POST.get('task'):
            updateTask.task = request.POST.get('task')
        if request.POST.get('status'):
            updateTask.status = request.POST.get('status')
        if request.POST.get('comment'):
            updateTask.comment = request.POST.get('comment')
        updateTask.save()
        ##The above 4 if conditons are used beacause if we are updating comment then that is seperated form and send post request
        ## and it produce error while updating task,status,assigned_to_id and assigned_to_name
        ## as the post request will give None while retreiving data.

        if historyCheckFlag != False :
            historyDetail = GroupTaskActivityModel()                
            historyDetail.grpTaskActivity_id = updateTask
            #Here the grpTaskActivity_id is foreign key connected to TaskAssignModel

            if flag == True: ##This check is done to see if comment is changed or not
                historyDetail.comments = request.POST.get('comment')
            historyDetail.history = historyCheckFlag
            historyDetail.dateTime = datetime.now()
            historyDetail.updated_by = str(request.user)
            historyDetail.save()
            allUsers =  User.objects.all()


            assigned_to_userFlag,assigned_by_userFlag = False,False 
            for userData in allUsers:
                if userData.username == updateTask.assigned_to_name :
                    assigned_to_user = User.objects.get(username=userData.username)
                    assigned_to_userFlag = True

                if userData.username == updateTask.assigned_by :
                    assigned_by_user = User.objects.get(username=userData.username)
                    assigned_by_userFlag =True

                if assigned_to_userFlag and assigned_by_userFlag:
                    mail_subject = 'Group:-' + groupName + "\n'" + updateTask.task + "'" + ' task has been updated by ' + str(request.user) +  '\n' + 'Update-->\n' +historyCheckFlag
                    send_mail('Task Update',mail_subject,'djangoemail2020@gmail.com' , [assigned_to_user.email,assigned_by_user.email] , fail_silently=False)
                    break
            ##This whole process of for loop and 3 if conditionsa are done to retrieiv email of users
            ##To whom we need to send email
            

    task = updateTask.task
    assigned_to_id = updateTask.assigned_to_id_id
    assigned_to_name = updateTask.assigned_to_name
    status = updateTask.status
    comment = updateTask.comment
    assigned_by = updateTask.assigned_by
    ##This all values(task,assigend_to_id,etc) are seperated 
    ##Because this value are used to show on update task form

    mylist_data=ToDoModel.objects.filter(user=request.user,status='todo',flagTask='no')
    task_flag_update(request.user)

    delailedActivity = GroupTaskActivityModel.objects.filter(grpTaskActivity_id_id=id)
    #The detailedActivity contains all the GroupTaskActivityModel objects of task (which as id)

    return render(request,'todoapp/updateAssignedTask.html',
        {'id':id,'grpid':grpid,'historyFlag':historyFlag,'status':status,'allfiles':allfiles,'allLinks':allLinks,'formFile':formFile,'formLink':formLink,
        'current_user':request.user,'task':task,'grp_member':grp_member,'comment':comment,'delailedActivity':delailedActivity,
        'assigned_to_id':assigned_to_id,'data':mylist_data})


###################### This Function is used to attach files to tasks  #################################################################################################################
def fileAttachmentView(request,id=None,grpid=None):
    if request.method == 'POST':
        fileTask = TaskAssignModel.objects.get(id=id)
        form = GroupTaskAttachmentsForm(request.POST, request.FILES)
        if form.is_valid():
            add_file_id = form.save(commit=False)
            add_file_id.fileTask_id = fileTask
            add_file_id.save()

    return redirect('/updateAssignedTask/' + id + '/' + grpid )

#################  This Function is used to attach link to tasks ##########################################################################

def webLinkAttachmentView(request,id=None,grpid=None):
    if request.method == 'POST':
        fileTask = TaskAssignModel.objects.get(id=id)
        form = GroupTaskWebLinkForm(request.POST)
        if form.is_valid():
            add_link_id = form.save(commit=False)
            add_link_id.linkTask_id = fileTask
            add_link_id.save()


    return redirect('/updateAssignedTask/' + id + '/' + grpid )




############################################################################################################
############################################################################################################