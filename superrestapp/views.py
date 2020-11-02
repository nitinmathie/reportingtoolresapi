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
                data['username'] = user.password
        else:
            data['username'] = serializer.errors
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

@api_view(["POST"])    
def get_allusers(request):
    kept = []    
    username = request.data['username']
    student_list = User.objects.get(username=username)
    # for student in student_list:
    #     kept.append(student.username)
    #your_list_as_json = json.dumps(kept)
    return HttpResponse(student_list.user_id)   
        
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
            #request.POST._mutable = False
        except:
            return Response("Error")
        return JsonResponse(data, safe=False)
# Add Organization
#will add it
# Add Organization Profile

#Add Organization
@api_view(["POST"])
def add_organization_view(request):
    if request.method=='POST':
        username = request.data['username']
        organization_name = request.data['c']
        organization_email = request.data['organization_email']
        organization_address = request.data['organization_location']
        #organization_created_by = request.data['organization_location']
        #organization_updated_by = request.data['organization_location']
        user = User.objects.get(username=username)
        try:
            data={}
            organization_result={}
            data["organization_name"] = organization_name
            data["organization_email"] = organization_email
            data["organization_address"] = organization_address
            data["organization_created_by"] = user.user_id
            data["organization_updated_by"] = user.user_id
            organization_created_by = user.user_id
            organization_updated_by = user.user_id
            users=[]
            users.append(user)
            users[0]
            x=[]
            u={}
            u["user_id"]=users[0].user_id
            u["username"]=users[0].username
            u["user_email"]=users[0].user_email 
            x.append(u)  
            data["organization_users"] = x                     
            org = Organization.objects.create(organization_name=organization_name,
            organization_email=organization_email,
             organization_updated_by_id=user.user_id, 
             organization_created_by_id=user.user_id)
            org.organization_users.set(users)
            orgcount = Organization.objects.filter(organization_name=organization_name).count()
            if orgcount>=2:
                return Response(request.data['organization_name']+' exists' + ' Choose another username')
            else:
                o = org.save()
                organizations = Organization.objects.get(organization_name=organization_name)
                serializer = OrganizationSerializer(organizations, many=False)                
                organization_result['organization'] = serializer.data
                dat={}
                organization_result['isSuccessful']=True 
                organization_result['user'] =username
                organization_result['userRole'] ="Admin"
                organization_result['message'] ="Success"

        except:
            organization_result={}
            organization_result['error']  ="error"      

        #    request.POST._mutable = False
            #data = serializer.errors
        return Response(organization_result)
#check : users not getting added

@api_view(["POST"])
def get_organizations_view(request):
    if request.method =='POST':
        username = request.data['username']
        user = User.objects.get(username=username)
        userid = user.user_id
        dat ={}
        org=[]
        organization = {}
        user_organizations = Organization.objects.all()
        dat['isSuccessful']=True 
        dat['user'] =request.data['username']
        dat['userRole'] ="Admin"
        dat['message'] ="Success"
        organizationusers=[]
        usr={}
        org=[]
        for o in user_organizations:
           
            organization = {}
            organization["organization_name"]=o.organization_name
            organization["organization_id"]=o.organization_id
            organization["organization_email"]=o.organization_email
            orgusers = o.organization_users.all()
            #org.append(organization)
            if orgusers.filter(user_id=userid).exists():                                
                org.append(organization)                    
        dat['organizations'] =org                     
    else:
        dat['serializer error'] = "some Error"        
    return Response(dat)

@api_view(["POST"])
def add_project_view(request):
    if request.method=='POST':
        project_result={}
        username = request.data['username']
        user = User.objects.get(username=username)
        project_name=request.data['project_name']
        organization_name=request.data['organization_name']
        organization = Organization.objects.get(organization_name=organization_name)
        organization_project_id=organization.organization_id
        project_type = request.data['project_type'] 
        project_location = request.data['project_location']        
        project_description = request.data['project_description']
        project_created_by = user.user_id
        project_updated_by = user.user_id
        users=[]
        users.append(user)
        x=[]
        u={}
        u["user_id"]=users[0].user_id
        u["username"]=users[0].username
        u["user_email"]=users[0].user_email 
        x.append(u)         
        res=[]
        dat={}
        createProject= Project.objects.create(project_name=project_name,
        organization_project_id_id=organization_project_id,
        project_created_by_id=user.user_id,
        project_updated_by_id=user.user_id,
        project_type=project_type,project_location=project_location,project_description=project_description
        )
        createProject.project_users.set(users)
        projCount = Project.objects.filter(project_name=project_name).count()
        if projCount>=2:
            return Response(request.data['project_name']+' exists' + ' Choose another username')
        else:
            savedProject = createProject.save()     
            projects = Project.objects.get(project_name=project_name)
            serializer = ProjectSerializer(projects, many=False)                
            project_result['project'] = serializer.data
            dat={}
            project_result['isSuccessful']=True 
            project_result['user'] =username
            project_result['userRole'] ="Admin"
            project_result['message'] ="Success"                          
        return Response(project_result)
@api_view(["POST"])
def get_projects_view(request):
    if request.method =='POST':
        username = request.data['username']
        organization_name = request.data['organization_name']
        user = User.objects.get(username=username)
        userid = user.user_id
        organization = Organization.objects.get(organization_name=organization_name)
        organization_id=organization.organization_id
        projects = Project.objects.filter(organization_project_id=organization_id)
        dat ={}        
        project = {}
        usrs=[]
        proj=[]
        for pro in projects:
            project={}           
            u = pro.project_users.all()
            project['projectid'] = pro.project_id
            project['project_name'] =pro.project_name
            project['project_type'] = pro.project_type 
            if u.filter(user_id=userid).exists():                                
                proj.append(project)                          
        dat['projects'] =  proj                            
        dat['isSuccessful']=True 
        dat['user'] =request.data['username']      
        dat['message'] ="Success"                                           
    else:
        dat['serializer error'] = "some Error"
    return Response(dat)

### Store
@api_view(["POST"])
def add_store_view(request):
    if request.method=='POST':
        store_result={}
        username = request.data['username']
        user = User.objects.get(username=username)
        store_name=request.data['store_name']
        store_project_id=request.data['store_project_id']
        store_organization_id=request.data['store_organization_id']
        store_location = request.data['store_location']        
        store_created_by = user.user_id
        store_updated_by = user.user_id
        users=[]
        users.append(user)
        x=[]
        u={}
        u["user_id"]=users[0].user_id
        u["username"]=users[0].username
        u["user_email"]=users[0].user_email 
        x.append(u)         
        res=[]
        dat={}
        createStore= Store.objects.create(store_name=store_name,
        store_project_id_id=store_project_id,
        store_organization_id_id= store_organization_id,
        store_created_by_id=user.user_id,
        store_updated_by_id=user.user_id,        
        )
        createStore.store_users.set(users)
        storeCount = Store.objects.filter(store_name=store_name).count()
        if storeCount>=2:
            return Response(request.data['store_name']+' exists' + ' Choose another username')
        else:
            savedStore = createStore.save()     
            stores = Store.objects.get(store_name=store_name)
            serializer = StoreSerializer(stores, many=False)                
            store_result['store'] = serializer.data
            dat={}
            store_result['isSuccessful']=True 
            store_result['user'] =username
            store_result['userRole'] ="Admin"
            store_result['message'] ="Success"                          
        return Response(store_result)
##getstore        
@api_view(["POST"])
def get_stores_view(request):
    if request.method =='POST':
        username = request.data['username']
        organization_name = request.data['organization_name']
        user = User.objects.get(username=username)
        userid = user.user_id
        organization = Organization.objects.get(organization_name=organization_name)
        organization_id=organization.organization_id
        stores = Store.objects.filter(store_organization_id=organization_id)
        dat ={}        
        store = {}
        usrs=[]
        stor=[]
        for pro in stores:
            store={}           
            u = pro.store_users.all()
            store['storeid'] = pro.store_id
            store['store_name'] =pro.store_name
            store['store_location'] = pro.store_location 
            if u.filter(user_id=userid).exists():                                
                stor.append(store)                          
        dat['stores'] =  stor                            
        dat['isSuccessful']=True 
        dat['user'] =request.data['username']      
        dat['message'] ="Success"                                           
    else:
        dat['serializer error'] = "some Error"
    return Response(dat)
## Add and Get users

@api_view(["POST"])
def get_users_view(request):
    if request.method =='POST':
        username = request.data['username']
        organization_name = request.data['organization_name']
        #user = User.objects.get(username=username)
        #userid = user.user_id
        organization = Organization.objects.get(organization_name=organization_name)
        organization_id = organization.organization_id
        #organization = Organization.objects.filter(organization_id=organization_id)
        organizationusers= organization.organization_users
        dat ={}        
        organization = {}
        usrs=[]

        for pro in organizationusers.all():
            user={}                       
            user['user_id'] = pro.user_id
            user['username'] =pro.username
            user['first_name'] = pro.first_name
            user['profile_completed_status'] = pro.profile_completed_status
            usrs.append(user)                         
        dat['users'] =  usrs                            
        dat['isSuccessful']=True 
        dat['user'] =request.data['username']      
        dat['message'] ="Success"   
        dat['organization'] =organization_id                                           
    else:
        dat['serializer error'] = "some Error"
    return Response(dat)
#add user
@api_view(["POST"])
def add_user_view(request):
    if request.method=='POST':
        project_result={}
        username = request.data['username']
        project_name=request.data['project_name']
        organization_name=request.data['organization_name']
        project = Project.objects.get(project_name=project_name)
        project_id= project.project_id
        organization = Organization.objects.get(organization_name=organization_name)
        organization_id= organization.organization_id                        
        user_role = request.data['user_role'] # choices field with all the construction fields available    
        first_name = request.data['first_name']        
        last_name = request.data['last_name']
        address = request.data['address']
        createUser= User.objects.create(username=username,
        first_name=first_name,
        last_name=last_name,
        address=address        
        )
        userCount = User.objects.filter(username=username).count()
        if userCount>=2:
            return Response(request.data['username']+' exists' + ' Choose another username')
        else:
            savedUser = createUser.save()     
            user = User.objects.get(username=username)
            user_id=user.user_id 
            createUserRole= User_Role.objects.create(user_id=user_id,
            project_id=project_id,
            organization_id=organization_id,
            role=user_role        
            )
            # check if a role exists if so update - Procrastinate this
            savedUserRole = createUserRole.save()
            userRole = User_Role.objects.get(user_id=user_id, organization_id=organization_id,
            project_id= project_id)
            organization = Organization.objects.get(organization_name=organization_name)
            usr ={}
            usr["user_id"]= user_id
            usr["username"]=username
            usr["role"]= userRole.role
            usr["organization_id"]= organization_id
            usr["project_id"]=  project_id 
            usr['isSuccessful']=True                                                 
        return Response(usr)

#Add Plan        
@api_view(["POST"])
def add_project_plan(request):
    if request.method=='POST':
        project_result={}
        username = request.data['username']
        user = User.objects.get(username=username)
        project_name=request.data['project_name']
        project = Project.objects.get(project_name=project_name)
        plan_project_id=project.project_id        
        organization_name=request.data['organization_name']
        organization = Organization.objects.get(organization_name=organization_name)
        plan_organization_id=organization.organization_id
        plan_name = request.data['plan_name']
       # plan_type = request.data['plan_type']   
        #plan_location = request.data['plan_location']        
        plan_description = request.data['plan_description']
        plan_created_by = user.user_id
        plan_updated_by = user.user_id
        createPlan= Plan.objects.create(plan_name=plan_name, plan_organization_id_id =plan_organization_id, plan_project_id_id = plan_project_id,
        plan_description=plan_description, plan_created_by_id=plan_created_by,plan_updated_by_id=plan_updated_by)
       
        planCount = Plan.objects.filter(plan_name=plan_name).count()
        if planCount>=2:
            return Response(request.data['plan_name']+' exists' + ' Choose another username')
        else:
            savedPlan = createPlan.save()     
            plans = Plan.objects.get(plan_name=plan_name)
            serializer = PlanSerializer(plans, many=False)                
            project_result['plan'] = serializer.data
            dat={}
            project_result['isSuccessful']=True 
            project_result['user'] =username
            project_result['userRole'] ="Admin"
            project_result['message'] ="Success"                          
        return Response(project_result)