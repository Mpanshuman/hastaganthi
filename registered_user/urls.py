from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('search',views.search,name = 'explore'),
    path('login',views.login_user,name = 'login'),
    path('register',views.registerUser,name = 'registeruser'),
    path('logout',views.logout_user,name = 'logout'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('userdetails/<int:pk>',views.userdetails,name='userdetails'),
    path('showimage/<int:pk>',views.showimage,name='showimage'),
    path('showprofile/<int:pk>',views.showprofile,name='showprofile'),
    path('choosemembership/<int:pk>',views.chooseMembership,name='choosemembership'),
    path('managemembership/<int:pk>',views.managemembership,name='managemembership'),
    path('interest',views.userInterest,name='interest'),
    path('deactivate',views.account_deactivate,name='deativateaccount'),
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)