from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def index(request):
    return render(request,'non_registered_user/index.html')


def contactus(request):
    return render(request,'non_registered_user/contactus.html')