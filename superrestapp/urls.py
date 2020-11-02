#from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import path
from .views import (userregistration_view,  gensend_otp, verify_otp, userlogin_view,get_allusers, get_organizations_view,
add_organization_view, add_project_view, get_projects_view, add_store_view, get_stores_view, get_users_view,add_user_view)

app_name= ""
urlpatterns = [
path('registration', userregistration_view, name= "register"),
path('sendotp',gensend_otp,name='sendotp'),
path('verifyotp',verify_otp,name='verifyotp'),
path('login',userlogin_view,name='login'),
path('getall',get_allusers, name='getall'),
path('getorganizations',get_organizations_view, name='getorganizations'),
path('addorganization',add_organization_view, name='addorganization'),
path('addproject',add_project_view, name='addproject'),
path('getprojects',get_projects_view, name='getprojects'),
path('addstore',add_store_view, name='addstore'),
path('getstores',get_stores_view, name='getstores'),
path('getusers',get_users_view, name='getusers'),
path('adduser',add_user_view, name='adduser'),
path('addplan',add_project_plan, name='addplan'),
]



