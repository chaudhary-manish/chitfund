from django.urls import path
from quickstart.API.views import *

app_name = 'quickstart'

urlpatterns =[

    path('',get_user_details,name='getdetails'),
    path('add',add_user_details,name='adddetails'),
    path('login',login_user,name='loginuser'),
    path('logout',logout_user,name='logoutuser'),
    path('addgroup',addgroup,name='addgroup'),
    path('addgroupuser',addgroupuser,name='addgroupuser')
]