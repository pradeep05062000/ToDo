from datetime import datetime,time
from todoapp.models import ToDoModel,TaskAssignModel,GroupModel,GroupAdminsModel
from django.core.mail import send_mail



#################This function is used to check date and time is updated or not after submitting update form#####################
def task_detail_modifed(description,status,date,time,id):
    d,t,s,dis,flag1,flag2,flag3,flag4 = False,False,False,False,False,False,False,False
    mylist_data=ToDoModel.objects.get(id=id)
    now=datetime.now()
    preDate=date_format(str(mylist_data.date))
    preTime = time_format(str(mylist_data.time))
    date1 = date_format(str(date))
    time1=time_format(str(time))
    
    if str(date) != str(mylist_data.date):
        flag1 = True
        d = 'Due date was modified from {} to {} at {}, {}\n'.format(preDate,date1,now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower()) 

    if str(time) != str(mylist_data.time):
        flag2 = True
        t = ' Due time was modified from {} to {} at {}, {}\n'.format(preTime,time1,now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower()) 

    if mylist_data.status != status :
        flag3 = True
        s = "Status was modified from {} to {} at {}, {}\n".format(mylist_data.status,status,now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower())
    
    if mylist_data.description != description:
        flag4 = True
        dis = "Description was modified at {}, {}\n".format(now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower())
    
    flag = [str(flag1) , str(flag2) , str(flag3) , str(flag4)]      

    if d and t and s and dis:
        return d + s + t + dis , flag

    elif d and t and dis:
        return d + t + dis , flag

    elif t and s and dis:
        return t + s + dis, flag

    elif d and s and dis:
        return d + s + dis, flag

    elif d and t:
        return d + t, flag

    elif t and s:
        return t + s,flag

    elif d and s:
        return d + s,flag

    elif d and dis:
        return d + dis,flag

    elif t and dis:
        return t + dis,flag

    elif s and dis:
        return s + dis,flag

    elif d:
        return d,flag
    elif t:
        return t,flag
    elif s:
        return s,flag
    elif dis:
        return dis,flag
    else:
        return False,flag
    


######################This function is used to convert date in ( mmm dd, yyyy ) this format###################################
def date_format(date):
    modefied_date =''
    dict1={'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    date = date.split('-')

    modefied_date = dict1[date[1]] + ' ' + date[2] + ', ' + date[0]

    return modefied_date
 

########################This function is used to convert time in ( 12 hr ) format ###############################################

def time_format(time):
    
    time=time.split(':')
    modefied_time=''
    if int(time[0])>12:
        convert_12 = int(time[0]) - 12
        modefied_time= str(convert_12) + ":" + time[1] + " p.m."

    else:
        modefied_time=time[0] + ":" + time[1] + " a.m."

    return modefied_time



##########################This function is used to  check time in todo list is due or not##############################################



def task_flag_update(user):
    mylist_data = ToDoModel.objects.filter(user=user,status='todo',flagTask='no')

    current_date=str(datetime.now().date())+datetime.now().strftime("%H:%M")
    
    for task in mylist_data:
        tasktime=str(task.date)+task.time.strftime("%H:%M")
        if current_date == tasktime:
            task.flagTask = 'yes'
            task.save()

###################################Function to check group task comment is changed or not ########################################################

def historyCheck(recentComment,recentTask,recentStatus,memberId,id):
    oldData = TaskAssignModel.objects.get(id=id)
    ct,tk,ss,mid,flag=False,False,False,False,False

    print(recentTask)

    if oldData.comment != recentComment :
        if recentComment != None:
            flag = True
            ct = 'Comment:'+ recentComment + '\n'

    if oldData.task != recentTask:
        if recentTask != None:
            tk = 'Task:' + recentTask + '\n'

    if oldData.status != recentStatus:
        if recentStatus != None:
            ss = 'Status:' + recentStatus + '\n'

    if memberId != None:
        if oldData.assigned_to_id_id != int(memberId):
            member=GroupModel.objects.get(id=memberId)
            mid = 'Assigned To:' + str(member.member) + '\n'



    if ct and tk and ss and mid:
        return  tk + ss + ct + mid , flag

    elif ct and tk and ss:
        return tk + ss + ct , flag

    elif ct and tk and mid:
        return  tk+ct+ mid , flag

    elif ct and ss and mid:
        return  ss + ct + mid , flag

    elif tk and ss and mid:
        return tk + ss + mid , flag

    elif ct and tk:
        return  tk +ct  , flag

    elif ct and mid:
        return ct + mid , flag

    elif ss and mid:
        return ss + mid, flag

    elif ct and ss:
        return ss + ct  , flag

    elif mid and tk:
        return tk  + mid , flag

    elif ss and tk:
        return  tk + ss , flag

    elif ct:
        return ct , flag

    elif tk:
        return tk , flag

    elif ss:
        return ss, flag

    elif mid:
        return mid , flag

    else:
        return False, flag




######################This function is used to check current user are added in GroupAdminModel model or not#########################################

def verifyGroupAdmin(user):

    adminUsersData = GroupAdminsModel.objects.all()
    

    for data in adminUsersData:
        if data.adminUser == user:
            return True


    return False












        



