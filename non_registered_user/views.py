from django.shortcuts import render
from django.http import HttpResponse 
from registered_user.views import checkMembership,preferedusers

# Create your views here.

def index(request):
    checkMembership(request)
    if not request.user.is_anonymous:
        prefereduserdata = preferedusers(request)
        if prefereduserdata is not None:
            print('preferedUser:',prefereduserdata[0])
            print('imagedata:',prefereduserdata[1])
    return render(request,'non_registered_user/index.html')


def contactus(request):
    return render(request,'non_registered_user/contactus.html')
