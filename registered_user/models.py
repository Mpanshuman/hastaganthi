from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User_Details(models.Model):
    CREATEDFOR = (('Self','Self'),('Relative','Relative'))
    GENDER = (('Male','Male'),('Female','Female'),('Others','Others'))
    MiddleName = models.CharField(max_length=50,blank=True,null=True)
    createdfor = models.CharField(max_length=20,null=True,choices=CREATEDFOR)
    occupation = models.CharField(max_length=30,null=True)
    age = models.CharField(max_length=10,null=True)
    dateofbirth = models.DateField()
    religion = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField()
    gender = models.CharField(max_length=20,null=True,choices=GENDER)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    


class Parents_Details(models.Model):
    fathers_name = models.CharField(max_length=200,null=True)
    mothers_name = models.CharField(max_length=200,null=True)
    fathers_phn = models.CharField(max_length=20,null=True,blank=True)
    mothers_phn = models.CharField(max_length=20,null=True,blank=True)
    fathers_email = models.EmailField(max_length=200,null=True,blank=True)
    mothers_email = models.EmailField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.fathers_name


## Add model for photos