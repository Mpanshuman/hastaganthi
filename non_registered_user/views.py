from django.shortcuts import render
from django.http import HttpResponse 
from registered_user.views import checkMembership

# Create your views here.

def index(request):
    checkMembership(request)
    return render(request,'non_registered_user/index.html')


def contactus(request):
    return render(request,'non_registered_user/contactus.html')


def check_user(request):
    if request.user.is_anonymous:
        print('a')
    else:
        print('b')