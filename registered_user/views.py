from django.shortcuts import render,redirect
from registered_user.models import MyUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from non_registered_user.models import User_Test 
from registered_user.models import User_Details 
from django.contrib.auth.decorators import login_required
from random import randint
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import requests
from django.http import JsonResponse
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


        # {'Status': 'Success', 'Details': 'ddd8b058-da70-48ab-bdcf-e2a5fe50a359'}
        # otp = otp_gen(phone)
        # response = send_otp(request,phone=phone,otp=otp)
        # print(response)
        
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
    userphone = request.user.phone
    userdatafromdb = get_userdata(request)
    userdata = {'UserName': username,'UserEmail': useremail, 'UserData':userdatafromdb,'UserPhone':userphone}

    return render(request,'registered_user/userprofile.html',userdata)

## Checking for current user
# def cuuser(request):
#     current_user = request.user
#     print('current User is: ',current_user.username)

# OTP GENERATOR

def otp_gen(phone):
    if phone:
        otp = randint(999,9999)
        # print('OTP GENERATED: ',otp)
        return otp
    else:
        return False


# {"Status":"Success","Details":"9a34f389-e538-47a6-bf3a-80d097b29504"}

# Send OTP to the Registered Number if Valid
def send_otp(request,phone,otp):
    
    URL = f"https://2factor.in/API/V1/683f7e4e-191c-11eb-b380-0200cd936042/SMS/{phone}/{otp}/HASTA"
    
    response = requests.request('GET',URL)
    data = response.json()
    
    return data

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



def get_userdata(request):
    try:
        userdata = User_Details.objects.get(user_id=request.user.id)
    except User_Details.DoesNotExist:
        userdata = {'age':'-','dateofbirth':'-','religion':'-','gender':'-','profile_pic':'/images/defaultpic.png'}
    print('User Data:', userdata)
    return userdata