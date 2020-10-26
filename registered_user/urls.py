from django.urls import path
from . import views
urlpatterns = [
    path('search',views.search,name = 'explore'),
    path('login',views.login_user,name = 'login'),
    path('register',views.registerUser,name = 'registeruser'),
    path('logout',views.logout_user,name = 'logout'),
    path('userprofile',views.userprofile,name='userprofile')
    
]