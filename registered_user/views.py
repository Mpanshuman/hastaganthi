from django.shortcuts import render,redirect
from registered_user.models import MyUser, Image
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from non_registered_user.models import User_Test 
from registered_user.models import User_Details, Membership
from django.contrib.auth.decorators import login_required
from random import randint
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import requests
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from registered_user.forms import UserForm, ImageForm
from django.core.paginator import Paginator,EmptyPage
from .models import *
from datetime import date
from dateutil.relativedelta import relativedelta
# Create your views here.

@login_required
def search(request):
    query = request.GET.get('search')
    
    if query is None:
        userdetails = User_Details.objects.none()
    
    elif query == '':

        userdetails = User_Details.objects.none()
    
    elif len(query) > 50:

        userdetails = User_Details.objects.none()
    
    else:
        userdetails = User_Details.objects.filter(Q(FirstName__icontains= query) |
        Q(LastName__icontains= query))
    
    imagedata = get_imagedata(userdetails)

    userdataperpage = manage_page(request,list(zip(userdetails,imagedata)))

    membershipstatus = getmembershipstatus(request)
    
    param = {'userdetails':userdataperpage,'search':query,'membership':membershipstatus}    
    
    return render(request,'registered_user/explore.html',param)

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
       
        membership = Membership(user_id = myuser.id)
        membership.save()
        
        return redirect('index')
    
    else:
        return render(request,'registered_user/registeration_user.html')


def logout_user(request):
    
    logout(request)
    return redirect('index')


def userprofile(request):
    
    try:
        image_details= Image.objects.get(user_id= request.user.id)

    except Image.DoesNotExist:
        image_details = None
    
    try:
        membershipinfo = Membership.objects.get(user_id= request.user.id)
    except Membership.DoesNotExist:
        image_details = None

    username = request.user.username
    useremail = request.user.email
    userphone = request.user.phone
    userdatafromdb = get_userdata(request)
    userdata = {'UserName': username,'UserEmail': useremail, 'UserData':userdatafromdb,'UserPhone':userphone,'image_details':image_details, 'membership':membershipinfo}
    
    return render(request,'registered_user/userprofile.html',userdata)




def userdetails(request,pk):
    try:
        userdata = User_Details.objects.get(user_id = pk)
    except User_Details.DoesNotExist:
        userdata = None
        
    if userdata is not None:
        form = UserForm(instance = userdata)
    else:
        form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, instance=userdata)
        if form.is_valid():
            userdetailsform = form.save(commit=False)
            userdetailsform.user = request.user
            userdetailsform.save()

            
            return redirect('userprofile')

    return render(request,'registered_user/personaldetailsform.html',{'form':form})


def showprofile(request,pk):
    try:
        userdata = User_Details.objects.get(id = pk)
        
    except User_Details.DoesNotExist:
        userdata = None
        
    try:
        imagedata = Image.objects.get(user_id = userdata.user_id)
    except Image.DoesNotExist:
        imagedata = None
    
    membershipstatus = getmembershipstatus(request)


    # print('userdata:',imagedata.imagefile)
    userdata = {'userdata': userdata,'image': imagedata,'default':'images/default_pic.png','membership':membershipstatus}
    return render(request,'registered_user/showprofile.html',userdata)



def chooseMembership(request,pk):
    if request.method == 'POST':
        sub_months = request.POST['btn']
        # print('btn:',months)
        if sub_months is not None:
            
            try:
                membershipdata = Membership.objects.get(user_id = pk)
            except Membership.DoesNotExist:
                membershipdata = None
            
            if membershipdata is not None and membershipdata.membership_start_data is None:
                membershipdata.membership = 'Premium'
                membershipdata.membership_start_data = date.today()
                membershipdata.membership_end_data = membershipdata.membership_start_data + relativedelta(months=+int(sub_months))
                membershipdata.save()
                return redirect('userprofile')
            else:
                membershipdata.membership = 'Premium'
                membershipdata.membership_end_data = membershipdata.membership_end_data + relativedelta(months=+int(sub_months))
                membershipdata.save()
                return redirect('userprofile')



    return render(request,'registered_user/choosemembership.html')


def managemembership(request,pk):
    try:
        membershipdata = Membership.objects.get(user_id = pk)
    except Membership.DoesNotExist:
        membershipdata = None
    
    if request.method == 'POST':
    
        membershipchoise = request.POST['btn']
        print('membershipchoise: ',membershipchoise)
        if membershipchoise == 'cancel':

            membershipdata.membership = 'Free'
            membershipdata.membership_start_data = None
            membershipdata.membership_end_data = None
            membershipdata.save()
            return redirect('userprofile')

            print('cancel')
        else:
            print('extend')
    
    membershipdata_context = {'membership':membershipdata}



    return render(request,'registered_user/managemembership.html',membershipdata_context)




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
        userdata = {'age':'-','dateofbirth':'-','religion':'-','gender':'-'}
    
    
    return userdata


def manage_page(request,searchresult):
    
    p = Paginator(searchresult,2)
    pagenum = request.GET.get('page',1)
    
    try:
        page = p.page(pagenum)
    except EmptyPage:
        page = p.page(1)
    
    return page



#for image
def showimage(request,pk):
    
    try:
        imagefile= Image.objects.get(user_id= pk)
        
    except Image.DoesNotExist:
        imagefile = None
        


    if imagefile is not None:
        form = ImageForm(instance = imagefile)
    else:
        form = ImageForm()
    if request.method == 'POST':
        form= ImageForm(request.POST,request.FILES,instance = imagefile)
        if form.is_valid():
            imageviewform = form.save(commit = False)
            imageviewform.user = request.user
            imageviewform.save()
            
            return redirect('userprofile')

    
    context= {'imagefile': imagefile,
              'form': form
              }
    
      
    return render(request, 'registered_user/images_try.html', context)


#get image
def get_imagedata(userdetails):

    userdetails_value =  userdetails.values('user_id')
   
    res_lis = []
    user_list = [uid['user_id'] for uid in userdetails_value ]
    
    imgdetails = Image.objects.filter(user_id__in = user_list)
   
    imgdetails_values = imgdetails.values()
    
    imgdetails_values_id = imgdetails.values('user_id')
    
    img_list = [uid['user_id'] for uid in imgdetails_values_id ]
   
    for data in user_list:

        if data in img_list:
            res_lis.append('media/'+str(Image.objects.get(user_id = data).imagefile))
        else:
            res_lis.append("media/images/default_pic.png")

    return res_lis


def checkMembership(request):
    if not request.user.is_anonymous:
        today = date.today()
        membershipdata = Membership.objects.get(user_id = request.user.id)
        if membershipdata.membership != 'Free':

            if today > membershipdata.membership_end_data:
                membershipdata.membership = 'Free'
                membershipdata.membership_start_data = None
                membershipdata.membership_end_data = None
                membershipdata.save()
            print('membership:', membershipdata.membership)
        else:
            print('free membership')


def getmembershipstatus(request):
    if not request.user.is_anonymous:
        membershipdata = Membership.objects.get(user_id = request.user.id)
        print(membershipdata.membership)
        return membershipdata



