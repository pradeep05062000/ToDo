from django import forms
from todoapp.models import ToDoModel
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth import authenticate

def name_exist(value):                ######This is the  custom validators to validate is username already exists or not
    flag=True
    try:                                ############
        User.objects.get(username=value)### This User.objects.get(username=value) is used to check the user is present inside model or not
    except:                             ###If it is present then flag vale will not change else it will set to false
        flag=False                      ##############

    if flag==True:
        raise forms.ValidationError('This name already exist')
#########
class SignUpForm(forms.ModelForm):
    username=forms.CharField(validators=[name_exist])
    class Meta:
        model=User
        fields=['username','password','first_name','last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }


###############################################################################################################################


class ResetPasswordForm(forms.Form):
    oldp=forms.CharField(max_length=32, label='Old Password', widget=forms.PasswordInput)
    newp=forms.CharField(max_length=32, label='New Password', widget=forms.PasswordInput)
    checkp=forms.CharField(max_length=32, label='Re-Enter(Password)', widget=forms.PasswordInput)


    def __init__(self,*args,request=None,**kwargs):
        self.request=request
        super().__init__(*args, **kwargs)

    def clean_oldp(self):
        password=self.cleaned_data['oldp']
        user = authenticate(username=self.request.user, password=password)  #### To check password of particular user we use authenticate function
        if user == None:
            raise forms.ValidationError("Old Password is Wrong")


    def clean(self):
        total_cleaned_data=super().clean()
        newp=total_cleaned_data['newp']
        checkp=total_cleaned_data['checkp']

        if newp!=checkp:
            raise forms.ValidationError("Password Does Not Match")




 

