from django.shortcuts import render,redirect
from django.contrib.auth.models import User
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
        # register(request)
        user = authenticate(username = username , password = password)
        msg = str(username) + ' ' + str(password) + ' ' +str(user)
        if user is not None:
            login(request,user)
            messages.info(request, 'exists')
            return redirect('index')
        else:
            messages.info(request,msg)
            return redirect('login')

    else:
        return render(request,'registered_user/login.html')


def registerUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['emailaddress']
        myuser = User.objects.create_user(username = username, email = email, password = password)
        custdb = User_Test(username = username,password = password, phone= phone)
        myuser.save()
        custdb.save()
        print('User Added')
        print('Data Added in db')
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
    print(userdata)
    return render(request,'registered_user/userprofile.html',userdata)

## Checking for current user
# def cuuser(request):
#     current_user = request.user
#     print('current User is: ',current_user.username)