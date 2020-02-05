from django.urls import path
from quickstart.API.views import get_user_details,add_user_details

app_name = 'quickstart'

urlpatterns =[

    path('',get_user_details,name='getdetails'),
    path('add',add_user_details,name='adddetails')
]