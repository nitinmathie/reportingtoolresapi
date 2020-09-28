# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.response import Response
from superrestapp.models import *
from superrestapp.serializers import *
from rest_framework.decorators import api_view

from django.http import HttpResponse

import bcrypt
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json

#user registration
@api_view(["POST"])
def userregistration_view(request):
    #Pending: when the registration fails the userprofile if created has to be deleted.
    if request.method == 'POST':
       # request.POST._mutable = True
        password= request.data['password'].encode('utf-8')
        pwdhash= bcrypt.hashpw(password, bcrypt.gensalt())
        #pwdhashencode = pwdhash.encode('utf-8')
        request.data['password']=pwdhash.decode('utf-8')
        serializer = UserSerializer(data=request.data)
        data = {}
        userResponse ={}
        if serializer.is_valid():
            username = request.data['username']
            usercount = User.objects.filter(username=username).count()
            if usercount>=1:
                return Response(request.data['username']+' exists' + ' Choose another username')
            else:

                user = serializer.save()
                #bcrypt.checkpw(password,pwdhash)
                data['isSuccessful']=True 
                userResponse['email'] =user.user_email
                userResponse['firstname'] =user.username
                #userResponse['projects']=user.userProjects
                #userResponse['organizations']=user.userOrganizations
                data['user'] = userResponse
        else:
            data['username'] = request.data['password']
        #    request.POST._mutable = False
            #data = serializer.errors
        return Response(data)
#generate otp and send otp
@api_view(["POST"])
def gensend_otp(request):
    if request.method == 'POST':
        email = request.data['email']
        otp = mailotp(email)        
        request.data['otp'] = otp
        otpserializer = OtpSerializer(data=request.data)
        if otpserializer.is_valid():
            try :
                otps = Otp.objects.filter(email=email)
                if otps.count()>=1:
                    otps.delete()
                otp = otpserializer.save()
            except :
                otp = otpserializer.save()
        try:
            otpreceived = mailotp(email)            
            return Response(otpreceived)
        except:
            return Response("Error")
@api_view(["POST"])
def verify_otp(request):
    if request.method == 'POST':
        email = request.data['email']
        otp = request.data['otp']
        otps = Otp.objects.filter(email=email).order_by('-created_at')
        if otps.count()>=1:
            verifyotp = otps[0]
            if str(otp)==str(verifyotp.otp):
                return Response(1)
            else:
                return Response(otp)

        else:
           return Response("Otp has never been generated")
        #return Response("")
#mail otp
def mailotp(mailid):

    from_address = 'nithunitin@gmail.com'

    to_address = str(mailid)

    message = MIMEMultipart('Foobar')

#    epos_liggaam['Subject'] = 'Foobar'

    message['From'] = from_address

    message['To'] = to_address
    otp = otpgenerator()
    content = MIMEText(str(otp), 'plain')

    message.attach(content)

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(from_address, 'N1t!nwonffa')

    mail.sendmail(from_address,to_address, message.as_string())

    mail.close()
    return otp
#    except:
#        return Response("MailError")
#otp generation
def otpgenerator():    
    #if request.method == 'POST':
    #email= request.data['email']
    otp = randint(999,10000)        
    return otp
def get_allusers(request):
    kept = []
    student_list = User.objects.all()
    for student in student_list:
        kept.append(student.username)
    #your_list_as_json = json.dumps(kept)
    return HttpResponse(kept)   
        
#user login
@api_view(["POST"])
def userlogin_view(request):
    if request.method == 'POST':
        request.POST._mutable = True
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        data = {}
        userResponse ={}
        try:
            pwd = user.password.encode('utf-8')
            password = password.encode('utf-8')    
            x = bcrypt.checkpw( password, pwd)
            data['isSuccessful']=x 
            userResponse['email'] =user.user_email
            userResponse['firstname'] =user.username
            #userResponse['projects']=user.userProjects
            #userResponse['organizations']=user.userOrganizations
            data['user'] = userResponse
            request.POST._mutable = False
        except:
            return Response("Error")
        return JsonResponse(data, safe=False)
# Add Organization
#will add it
# Add Organization Profile

#Get Organization
@api_view(["POST"])
def get_organizations_view(request):
    if request.method =='POST':
        user = request.data['username']
        data ={}
        #org={}
        organization = {}
        data['isSuccessful']=True
        data['user'] = "user"
        data['userRole'] = "Admin"
        organization['organization_name'] ="Hello"
        organization['organization_id'] =1
        #data['organization'] = organization
        return Response(data)

