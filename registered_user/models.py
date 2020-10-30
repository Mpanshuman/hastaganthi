from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
import datetime

class MyUserManager(BaseUserManager):
    
    def create_user(self, email, phone,username, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone,username, password=None):
           
        user = self.create_user(email,password=password,phone=phone,username=username,)
        user.is_admin = True
        user.save(using=self._db)
        return user

# created Custom model for User Creation 

class MyUser(AbstractBaseUser):
    
    username = models.CharField(verbose_name='username',
                                max_length=255,null=True)
    
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True
    
                              )
    phone = models.CharField(verbose_name='mobile number',
                             max_length=15,
                             unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# Create your models here.


class User_Details(models.Model):
    
    CREATEDFOR = (('Self','Self'),('Relative','Relative'))
    GENDER = (('Male','Male'),('Female','Female'),('Others','Others'))
    FirstName = models.CharField(max_length=50,null=True)
    MiddleName = models.CharField(max_length=50,blank=True,null=True)
    LastName = models.CharField(max_length=50,null=True)
    createdfor = models.CharField(max_length=20,null=True,choices=CREATEDFOR)
    occupation = models.CharField(max_length=30,null=True)
    age = models.CharField(max_length=10,null=True)
    dateofbirth = models.DateField(default =datetime.date.today)
    religion = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField()
    gender = models.CharField(max_length=20,null=True,choices=GENDER)
    profile_pic = models.ImageField(null=True,blank=True,default = 'registered_user/images/defaultpic.png')
    user = models.ForeignKey(MyUser,null=True,on_delete=models.CASCADE)
    
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
    user = models.ForeignKey(MyUser,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.fathers_name


# Add model for photos