from django.shortcuts import render,redirect
from registered_user.models import MyUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from non_registered_user.models import User_Test 
from django.contrib.auth.decorators import login_required
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