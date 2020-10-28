from django.shortcuts import render,redirect
from registered_user.models import MyUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from non_registered_user.models import User_Test 
from django.contrib.auth.decorators import login_required
from random import randint
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import *
# Create your views here.

@login_required
def search(request):
    return render(request,'registered_user/explore.html')


def login_user(request):
    
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpassword']
        user = authenticate(email = username , password = password)
        
        if user is not None:
            login(request,user)
            otp_gen(username)
            return redirect('index')
              
        else:
            return redirect('login')

    else:
        return render(request,'registered_user/login.html')


def registerUser(request):
    
    if request.method == 'POST':

        # Getting Values from html form by name
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['emailaddress']

        # creating user in MyUser model(Custom model)
       
        myuser = MyUser.objects.create_user( username=username,email = email, password = password, phone=phone)

        ## Like above add Data in Personal,Parents and preference model
        # preference model not created yet...
        
        '''sent_mail will work for less secure app(gmail > account setting > less secure app > enabled)'''
        #sent_email(username=username,email=email)
        myuser.save()
        return redirect('index')
    
    else:
        return render(request,'registered_user/registeration_user.html')


def logout_user(request):
    
    logout(request)
    return redirect('index')


def userprofile(request):
    
    username = request.user.username
    useremail = request.user.email
    userdata = {'UserName': username,'UserEmail': useremail}
    return render(request,'registered_user/userprofile.html',userdata)

## Checking for current user
# def cuuser(request):
#     current_user = request.user
#     print('current User is: ',current_user.username)

# OTP GENERATOR

def otp_gen(phone):
    if phone:
        otp = randint(999,9999)
        print('OTP GENERATED: ',otp)
        return otp
    else:
        return False



'''sent_mail will work for less secure app(gmail > account setting > less secure app > enabled) 
   uncomment the sent_mail method to test
   settings.py > EMAIL_HOST_USER = 'Your Email Address'
                 EMAIL_HOST_PASSWORD = 'Your Email Address Password'
    
'''
def sent_email(username,email):
    template = render_to_string('registered_user/email_conformation.html',{'name':username})
    
    email = EmailMessage(
    'Thank you for choosing this site',
    template,
    settings.EMAIL_HOST_USER,
    [email],)
    email.fail_silently = False
    email.send()

   