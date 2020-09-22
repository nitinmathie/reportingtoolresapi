#from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import path
from .views import (userregistration_view,  gensend_otp, verify_otp, userlogin_view,)

app_name= ""
urlpatterns = [
path('registration', userregistration_view, name= "register"),
path('sendotp',gensend_otp,name='sendotp'),
path('verifyotp',verify_otp,name='verifyotp'),
path('login',userlogin_view,name='login'),
]



