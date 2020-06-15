from datetime import datetime
from todoapp.models import ToDoModel


#################This function is used to check date and time is updated or not after submitting update form#####################
def task_detail_modifed(disciption,status,date,time,id):
    d,t,s,dis = False,False,False,False
    mylist_data=ToDoModel.objects.get(id=id)
    now=datetime.now()
    preDate=date_format(str(mylist_data.date))
    preTime = time_format(str(mylist_data.time))
    date1 = date_format(date)
    time1=time_format(time)

    if date != str(mylist_data.date):
        d = 'Due date was modified from {} to {} at {}, {}\n'.format(preDate,date1,now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower()) 

    if time != str(mylist_data.time):
        t = ' Due time was modified from {} to {} at {}, {}\n'.format(preTime,time1,now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower()) 

    if mylist_data.status != status :
        s = "Status was modified from {} to {} at {}, {}\n".format(mylist_data.status,status,now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower())
    
    if mylist_data.discription != disciption :
        dis = "Discription was modified at {}, {}\n".format(now.strftime("%b %d, %Y"),now.strftime("%I:%M %p").lower())
 

    if d and t and s and dis:
        return d + s + t + dis

    elif d and t and dis:
        return d + t + dis

    elif t and s and dis:
        return t + s + dis

    elif d and s and dis:
        return d + s + dis

    elif d and t:
        return d + t

    elif t and s:
        return t + s

    elif d and s:
        return d + s 

    elif d and dis:
        return d + dis

    elif t and dis:
        return t + dis

    elif s and dis:
        return s + dis

    elif d:
        return d
    elif t:
        return t
    elif s:
        return s
    elif dis:
        return dis
    


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



#########################################################################################################


def discription_modefied(disciption,id):
    mylist_data=ToDoModel.objects.get(id=id)
    print(disciption,mylist_data.discription)
    if mylist_data.discription != disciption :
        return True



