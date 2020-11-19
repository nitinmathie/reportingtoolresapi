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
        organization_name = request.data['organization_name']
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
#get_plan
@api_view(["POST"])
def get_project_plans(request):
    if request.method =='POST':
        username = request.data['username']
        organization_name = request.data['organization_name']
        organization = Organization.objects.get(organization_name=organization_name)
        organization_id = organization.organization_id
        project_name = request.data['project_name']
        project = Project.objects.get(project_name=project_name)
        project_id = project.project_id        
        project_plans = Plan.objects.filter(plan_project_id_id=project_id, plan_organization_id_id=organization_id)
        #organization = Organization.objects.filter(organization_id=organization_id)
        organizationusers= organization.organization_users
        dat ={}        
        organization = {}
        plns=[]
        for plane in project_plans:
            plan={}                       
            plan['plan_id'] = plane.plan_id
            plan['plan_name'] =plane.plan_name
            plan['plan_description'] = plane.plan_description
            #plan['profile_completed_status'] = pro.profile_completed_status
            plns.append(plan)                         
        dat['plans'] =  plns                            
        dat['isSuccessful']=True 
        dat['user'] =request.data['username']      
        dat['message'] ="Success"   
        dat['organization'] =organization_id                                           
    else:
        dat['serializer error'] = "some Error"
    return Response(dat)        
#add task and activity
@api_view(["POST"])
def add_task(request):
    if request.method=='POST':  
        activity_result={}      
        username = request.data['username']
        user = User.objects.get(username=username)
        organization_name = request.data['organization_name']
        organization = Organization.objects.get(organization_name=organization_name)
        task_organization_id = organization.organization_id
        project_name = request.data['project_name']
        project = Project.objects.get(project_name=project_name)
        task_project_id = project.project_id
        #plan_name = request.data['plan_name']
        #plan = Plan.objects.get(project_name=project_name)
        #plan_project_id = plan.Plan_id                
        task_plan_id = request.data['plan_id']               
        task_name=request.data['task_name']        
        task_startnode=request.data['task_startnode']     
        task_endnode = request.data['task_endnode'] 
        createTask= Task.objects.create(task_name=task_name,
         task_organization_id_id =task_organization_id, 
         task_project_id_id = task_project_id,
         task_plan_id_id = task_plan_id,
         task_startnode = task_startnode, 
         task_endnode= task_endnode ,         
         task_created_by_id=user.user_id,
         task_updated_by_id=user.user_id)       
        taskCount = Task.objects.filter(task_name=task_name).count()
        if taskCount>=2:
            return Response(request.data['task_name']+' exists' + ' Choose another name for task')
        else:
            savedTask = createTask.save()                 
        task = Task.objects.get(task_name=task_name)            
        task_id = task.task_id                    
        ccbreaking_activity_name = "CCBreaking" + str(task_id)
        ccb_pipeline_trench_500_status = "0"
        ccb_mharea_status = "0"
        ccb_upvc_350= "0"
        ccb_IC_500 = "0"
        createActivity= CCBreakingActivity.objects.create(
                                cc_task_id_id = task_id,
                                ccbreaking_activity_name=ccbreaking_activity_name,
                                ccb_pipeline_trench_500_status =ccb_pipeline_trench_500_status, 
                                ccb_mharea_status = ccb_mharea_status,
                                ccb_upvc_350 = ccb_upvc_350,
                                ccb_IC_500 = ccb_IC_500) 
        actCount = CCBreakingActivity.objects.filter(ccbreaking_activity_name=ccbreaking_activity_name).count()
        if actCount>=2:
            return Response(request.data['ccbreaking_activity_name']+' exists' + ' Choose another name')
        else:
            savedActivity = createActivity.save()   
            serializer = CCBreakingActivitySerializer(savedActivity, many=False)                                
            activity_result['ccb'] = serializer.data

        task_id = task_id                
        pipeline_activity_name = "Pipe"+str(task_id)
        trenching_pipeline = "0"
        bedding = "0"
        laying= "0"
        pipe_jointing = "0"
        back_filling= "0"                                
        createPipeActivity= PipeLineActivity.objects.create(
                            pipe_task_id_id = task_id,
                                pipeline_activity_name=pipeline_activity_name,
                                trenching_pipeline =trenching_pipeline, 
                                bedding = bedding,
                                laying = laying,
                                pipe_jointing = pipe_jointing,
                                back_filling=back_filling
                                ) 
        actCount = PipeLineActivity.objects.filter(pipeline_activity_name=pipeline_activity_name).count()
        if actCount>=2:
            return Response(request.data['pipeline_activity_name']+' exists' + ' Choose another name')
        else:
            savedPipedActivity = createPipeActivity.save()     
            serializer = PipeLineActivitySerializer(savedPipedActivity, many=False)                                          
            activity_result['pipeactivity'] = serializer.data
        manhole_activity_name = "MH " + str(task_id)            
        excavation = "0"
        removal_excess_soil = "0"
        dust_fill_PCC_below = "0"
        base_erection= "0"
        pipe_mhbase_connection = "0"
        haunching= "0"
        raiser_erection = "0"
        cone_erection= "0"
        fix_UPVC = "0"
        back_filling= "0"
        createActivity= ManholeActivity.objects.create(
                                mh_task_id_id = task_id,
                                manhole_activity_name = manhole_activity_name,
                                excavation=excavation,
                                removal_excess_soil =removal_excess_soil, 
                                dust_fill_PCC_below = dust_fill_PCC_below,
                                base_erection = base_erection,
                                pipe_mhbase_connection = pipe_mhbase_connection,
                                haunching=haunching,
                                raiser_erection =raiser_erection, 
                                cone_erection = cone_erection,
                                fix_UPVC = fix_UPVC,
                                back_filling = back_filling
                                ) 
        actCount = ManholeActivity.objects.filter(manhole_activity_name=manhole_activity_name).count()
        if actCount>=2:
            return Response(request.data['manhole_activity_name']+' exists' + ' Choose another name')
        else:
            savedMHActivity = createActivity.save()     
            serializer = ManholeActivitySerializer(savedMHActivity, many=False)                
            activity_result['MHactivity'] = serializer.data
                    
                #break                

        restoration_activity_name = "RoadRestoration"+ str(task_id )
        fill_with_dust = "0"
        fill_with_concrete = "0"
        below_road_300= "0"
        pcc_200_mh = "0"
        pcc_200_pl= "0"
        vcc_pl_200 = "0"
        vcc_UPVC_200= "0"
        vcc_IC_100 = "0"
        createActivity= RoadRestorationActivity.objects.create(rr_task_id_id = task_id,
                                restoration_activity_name = restoration_activity_name,
                                fill_with_dust=fill_with_dust,
                                fill_with_concrete =fill_with_concrete, 
                                below_road_300 = below_road_300,
                                pcc_200_mh = pcc_200_mh,
                                pcc_200_pl = pcc_200_pl,
                                vcc_pl_200=vcc_pl_200,
                                vcc_UPVC_200 =vcc_UPVC_200, 
                                vcc_IC_100 = vcc_IC_100
                                ) 
        actCount = RoadRestorationActivity.objects.filter(restoration_activity_name=restoration_activity_name).count()
        if actCount>=2:
            return Response(request.data['restoration_activity_name']+' exists' + ' Choose another name')
        else:
            savedRRActivity = createActivity.save()     
            serializer = RoadRestorationActivitySerializer(savedRRActivity, many=False)                
            activity_result['rractivity'] = serializer.data
                #break                            
        hsc_activity_name ="HSC" + str(task_id)
        excavation_for_IC = "0"
        PCC_below_IC = "0"
        erection_IC= "0"
        dust_filling = "0"
        createActivity= HSCActivity.objects.create(
                                hsc_activity_name = hsc_activity_name,
                                hsc_task_id_id = task_id,
                                excavation_for_IC=excavation_for_IC,
                                PCC_below_IC =PCC_below_IC, 
                                erection_IC = erection_IC,
                                dust_filling = dust_filling
                                ) 
        actCount = HSCActivity.objects.filter(hsc_activity_name=hsc_activity_name).count()
        if actCount>=2:
            return Response(request.data['hsc_activity_name']+' exists' + ' Choose another name')
        else:
            savedHscActivity = createActivity.save()     
            serializer = HSCActivitySerializer(savedHscActivity, many=False)                
            activity_result['hscactivity'] = serializer.data
        housekeeping_activity_name = "HK"+str(task_id)
        createActivity= HouseKeepingActivity.objects.create(hk_task_id_id = task_id,
                                housekeeping_activity_name = housekeeping_activity_name                               
                                ) 
        actCount = HouseKeepingActivity.objects.filter(housekeeping_activity_name=housekeeping_activity_name).count()
        if actCount>=2:
            return Response(request.data['housekeeping_activity_name']+' exists' + ' Choose another name')
        else:
            savedHKActivity = createActivity.save()     
            serializer = HouseKeepingActivitySerializer(savedHKActivity, many=False)                            
            activity_result['hkactivity'] = serializer.data
        activity_result['taskid'] = task_id           
        return Response(activity_result)            
    else:
        return Response("Error")    

# Assign a task to user

@api_view(["POST"])
def assign_task_activity(request):
    if request.method=='POST':
        username = request.data['username']
        user = User.objects.get(username=username)                
        task_id= request.data['task_id'] 
        activity_type_id = request.data['activity_type_id'] 
        assigned_by = request.data['assigned_by'] 
        assigned_on = request.data['assigned_on'] 
        assigned_to = request.data['assigned_to'] 
        assignto = User.objects.get(username=assigned_to)          
        estimated_timeline = request.data['estimated_timeline'] 
        skilled_man_power = request.data['skilled_man_power'] 
        skilled_man_hours = request.data['skilled_man_hours'] 
        unskilled_man_power = request.data['unskilled_man_power'] 
        unskilled_man_hours =  request.data['unskilled_man_hours'] 
        jcb_quantity = request.data['jcb_quantity'] 
        jcb_hours = request.data['jcb_hours'] 
        tractor_quantity = request.data['tractor_quantity'] 
        tracktor_hours = request.data['tracktor_hours'] 
        hydra_quantity = request.data['hydra_quantity'] 
        hydra_hours = request.data['hydra_hours'] 
        water_tanker_quantity = request.data['water_tanker_quantity'] 
        water_tanker = request.data['water_tanker'] 
        tractor_compressor_quantity = request.data['tractor_compressor_quantity'] 
        tractor_compressor_hours =  request.data['tractor_compressor_hours'] 
        other_machine_quantity = request.data['other_machine_quantity'] 
        other_machine_hours = request.data['other_machine_hours'] 
        
        assignActivity= AssignActivity.objects.create(
                    assign_task_id_id= task_id,
        activity_type_id =  activity_type_id,
        assigned_by = user.user_id,
        assigned_on = assigned_on,
        assigned_to = assignto.user_id, 
        estimated_timeline = estimated_timeline,
        skilled_man_power = skilled_man_power, 
        skilled_man_hours = skilled_man_hours,
        unskilled_man_power = unskilled_man_power, 
        unskilled_man_hours =  unskilled_man_hours, 
        jcb_quantity = jcb_quantity,
        jcb_hours = jcb_hours,
        tractor_quantity =tractor_quantity, 
        tracktor_hours = tracktor_hours,
        hydra_quantity = hydra_quantity, 
        hydra_hours = hydra_hours,
        water_tanker_quantity = water_tanker_quantity,
        water_tanker = water_tanker, 
        tractor_compressor_quantity = tractor_compressor_quantity,
        tractor_compressor_hours =  tractor_compressor_hours,
        other_machine_quantity = other_machine_quantity,
        other_machine_hours = other_machine_hours
           )       
        assignCount = AssignActivity.objects.filter(assign_task_id_id=task_id).count()
        if assignCount>=2:
            return Response('The task has already assigned')
        else:
            project_restult={}
            savedAssignActivity = assignActivity.save()     
            activities = savedAssignActivity.objects.get(task_id=task_id)
            serializer = AssignActivitySerializer(activities, many=False)                
            project_result['assigned_activity'] = serializer.data            
            project_result['isSuccessful']=True 
            project_result['user'] = username
            project_result['userRole'] ="Admin"
            project_result['message'] ="Success"                          
        return Response(project_result)

@api_view(["POST"])
def report_task_activity(request):
    if request.method=='POST':
        username = request.data['username']
        user = User.objects.get(username=username)                
        task_id= request.data['task_id'] 
        activity_type_id = request.data['activity_type_id'] 
        assigned_by = request.data['assigned_by'] 
        assigned_on = request.data['assigned_on'] 
        assigned_to = request.data['assigned_to'] 
        assignto = User.objects.get(username=assigned_to)          
        estimated_timeline = request.data['estimated_timeline'] 
        skilled_man_power = request.data['skilled_man_power'] 
        skilled_man_hours = request.data['skilled_man_hours'] 
        unskilled_man_power = request.data['unskilled_man_power'] 
        unskilled_man_hours =  request.data['unskilled_man_hours'] 
        jcb_quantity = request.data['jcb_quantity'] 
        jcb_hours = request.data['jcb_hours'] 
        tractor_quantity = request.data['tractor_quantity'] 
        tracktor_hours = request.data['tracktor_hours'] 
        hydra_quantity = request.data['hydra_quantity'] 
        hydra_hours = request.data['hydra_hours'] 
        water_tanker_quantity = request.data['water_tanker_quantity'] 
        water_tanker = request.data['water_tanker'] 
        tractor_compressor_quantity = request.data['tractor_compressor_quantity'] 
        tractor_compressor_hours =  request.data['tractor_compressor_hours'] 
        other_machine_quantity = request.data['other_machine_quantity'] 
        other_machine_hours = request.data['other_machine_hours'] 
        reportActivity= Report_Activity.objects.create(
         task_id_id= task_id,
        assigned_task_id_id = assigned_task_id,
        activity_type_id_id = activity_type_id,
        reported_by = reportee.user_id,
        reported_on = reported_on,
        finish_timeline = finish_timeline,
        skilled_man_power =skilled_man_power,
        skilled_man_hours = skilled_man_hours,
        unskilled_man_power = unskilled_man_power,
        unskilled_man_hours =  unskilled_man_hours,
        jcb_quantity = jcb_quantity,
        jcb_hours = jcb_hours,
        tractor_quantity = tractor_quantity,
        tracktor_hours = tracktor_hours,
        hydra_quantity = hydra_quantity,
        hydra_hours = hydra_hours,
        water_tanker_quantity = water_tanker_quantity,
        water_tanker = water_tanker,
        tractor_compressor_quantity = tractor_compressor_quantity,
        tractor_compressor_hours =    tractor_compressor_hours,
        other_machine_quantity = other_machine_quantity,
        other_machine_hours =     other_machine_hours,
        report_status = report_status
       )       

        reportCount = Report_Activity.objects.filter(task_id=task_id).count()
        if reportCount>=2:
            return Response('The report has been reported earlier.')
        else:
            report_restult={}
            savedReportActivity = reportActivity.save()     
            activities = savedReportActivity.objects.get(task_id=task_id)
            serializer = Report_ActivitySerializer(activities, many=False)                
            if task_type == "CC":
                task_id = task_id
                update_cc = CCBreakingActivity.objects.get(task_id=task_id)
                update_cc.status=request.data['status'] 
                update_cc.completed_on=request.data['completed_on'] 
                updated_activity = update_cc.save()
                serializer = CCBreakingActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['plan'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #sbreak
                
            if task_type == "Pipe":
                task_id = task_id                
                update_pipe = PipeLineActivity.objects.get(task_id=task_id)
                update_pipe.status=request.data['status'] 
                update_pipe.completed_on=request.data['completed_on'] 
                updated_activity = update_pipe.save()
                serializer = PipeLineActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['pipe'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "MH":
                task_id = task_id                
                update_mh = ManholeActivity.objects.get(task_id=task_id)
                update_mh.status=request.data['status'] 
                update_mh.completed_on=request.data['completed_on'] 
                updated_activity = update_mh.save()
                serializer = ManholeActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['Manhole'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "RR":
                task_id = task_id                
                update_rr = RoadRestorationActivity.objects.get(task_id=task_id)
                update_rr.status=request.data['status'] 
                update_rr.completed_on=request.data['completed_on'] 
                updated_activity = update_rr.save()
                serializer = RoadRestorationActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['RR'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "HSC":
                task_id = task_id                
                update_hsc = HSCActivity.objects.get(task_id=task_id)
                update_hsc.status=request.data['status'] 
                update_hsc.completed_on=request.data['completed_on'] 
                updated_activity = update_pipe.save()
                serializer = HSCActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['HSC'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "HK":
                task_id = task_id,                                
                update_hk = HSCActivity.objects.get(task_id=task_id)
                update_hk.status=request.data['status'] 
                update_hk.completed_on=request.data['completed_on'] 
                updated_activity = update_hk.save()
                serializer = HSCActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['HSC'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            report_restult['report_activity'] = serializer.data            
            report_restult['isSuccessful']=True 
            report_restult['user'] = username
            report_restult['userRole'] ="Admin"
            report_restult['message'] ="Success"                          
        return Response(report_restult)
## Fetch Task based on Id, Fetch tasks assigned to a user, Fetch tasks reported by a user.
# fetch all the tasks defined in a plan.
@api_view(["POST"])
def fetch_plan_tasks(request):
    if request.method=='POST':
        username = request.data['username']
        user = User.objects.get(username=username)                
        plan_id= request.data['plan_id'] 
        project_id = request.data['project_id'] 
        organization_id = request.data['organization_id'] 
        tasks = Task.objects.filter(task_project_id=project_id, task_organization_id = organization_id , task_plan_id = plan_id)        
        tasksinfo={}
        tasks=[]
        for task in tasks:
            task_info={}           
            #u = task
            task_info['task_id'] = task.task_id
            task_info['task_name'] =task.task_name
            task_info['store_location'] = task.store_location 
            task_info['task_startnode'] = task.task_startnode
            task_info['task_endnode'] =task.task_endnode
            task_info['task_type'] =task.task_type
            tasks.append(taskinfo)            
        dat['tasksinfo'] =  tasks                            
        dat['isSuccessful']=True 
        dat['user'] =request.data['username']      
        dat['message'] ="Success"                                           
    else:
        dat['serializer error'] = "some Error"
    return Response(dat)

#Fetch task activities
@api_view(["POST"])
def fetch_task_activities(request):
    if request.method=='POST':
        username = request.data['username']
        user = User.objects.get(username=username)                
        plan_id= request.data['plan_id'] 
        project_id = request.data['project_id'] 
        organization_id = request.data['organization_id'] 
        task_id = request.data['task_id']         
        task_startnode = request.data['task_startnode']                 
        task_endnode = request.data['task_endnode']                         
        tasks = Task.objects.filter(task_project_id=project_id, task_organization_id = organization_id ,
         task_plan_id = plan_id, task_startnode =task_startnode, task_endnode=task_endnode )        
        tasksinfo={}
        task_activities=[]        
        for task in tasks:
            activity_info={}           
            #u = task
            task_id =task.task_id
            task_type = task.task_type
            if task_type == "CC":
                get_cc = CCBreakingActivity.objects.get(task_id=task_id)
                serializer = CCBreakingActivitySerializer(get_cc, many=False)                
                activity_info['task_id']=task_id
                activity_info['task_type'] = task_type
                activity_info['activity'] =serializer.data    
                task_activities.append(activity_info)            
            if task_type == "Pipe":
                task_id = task_id                
                get_pipe = PipeLineActivity.objects.get(task_id=task_id)
                serializer = PipeLineActivitySerializer(get_pipe, many=False)                
                activity_info['task_id']=task_id
                activity_info['task_type'] = task_type
                activity_info['activity'] =serializer.data    
                task_activities.append(activity_info)            

            if task_type == "MH":
                get_mh = ManholeActivity.objects.get(task_id=task_id)
                serializer = ManholeActivitySerializer(get_mh, many=False)                
                activity_info['task_id']=task_id
                activity_info['task_type'] = task_type
                activity_info['activity'] =serializer.data    
                task_activities.append(activity_info)            

            if task_type == "RR":
                get_rr = RoadRestorationActivity.objects.get(task_id=task_id)
                serializer = RoadRestorationActivitySerializer(get_rr, many=False)                
                activity_info['task_id']=task_id
                activity_info['task_type'] = task_type
                activity_info['activity'] =serializer.data    
                task_activities.append(activity_info)            

            if task_type == "HSC":
                get_hsc = HSCActivity.objects.get(task_id=task_id)
                serializer = HSCActivitySerializer(get_hsc, many=False)                
                activity_info['task_id']=task_id
                activity_info['task_type'] = task_type
                activity_info['activity'] =serializer.data    
                task_activities.append(activity_info)            

            if task_type == "HK":
                get_hk = HSCActivity.objects.get(task_id=task_id)
                serializer = HSCActivitySerializer(get_hk, many=False)                
                activity_info['task_id']=task_id
                activity_info['task_type'] = task_type
                activity_info['activity'] =serializer.data    
                task_activities.append(activity_info)            
        task_info['task_activities'] = task_activities
        task_info['issuccessful'] = True
        task_info['user'] =request.data['username']      
        task_info['message'] ="Success"                                           
        return Response(task_info)
#Fetch the task activity
@api_view(["POST"])
def fetch_task_activity(request):    
    if request.method=='POST':
        username = request.data['username']
        user = User.objects.get(username=username)                
        plan_id= request.data['plan_id'] 
        project_id = request.data['project_id'] 
        organization_id = request.data['organization_id'] 
        task_id = request.data['task_id']  
        activity_id = request.data['activity_id']         
        task_startnode = request.data['task_startnode']                 
        task_endnode = request.data['task_endnode']                         
        tasks = Task.objects.filter(task_project_id=project_id, task_organization_id = organization_id ,
         task_plan_id = plan_id, task_id =task_id)
        activity_info={}
        if task_type == "CC":
            get_cc = CCBreakingActivity.objects.get(activity_id=activity_id)
            serializer = CCBreakingActivitySerializer(get_cc, many=False)                
            activity_info['task_id']=task_id
            activity_info['task_type'] = task_type
            activity_info['activity'] =serializer.data    
            return Response(activity_info)
            #break
        if task_type == "Pipe":
            task_id = task_id                
            get_pipe = PipeLineActivity.objects.get(activity_id=activity_id)
            serializer = PipeLineActivitySerializer(get_pipe, many=False)                
            activity_info['task_id']=task_id
            activity_info['task_type'] = task_type
            activity_info['activity'] =serializer.data    
            return Response(activity_info)
            #break

        if task_type == "MH":
            get_mh = ManholeActivity.objects.get(activity_id=activity_id)
            serializer = ManholeActivitySerializer(get_mh, many=False)                
            activity_info['task_id']=task_id
            activity_info['task_type'] = task_type
            activity_info['activity'] =serializer.data    
            return Response(activity_info)
            #break

        if task_type == "RR":
            get_rr = RoadRestorationActivity.objects.get(activity_id=activity_id)
            serializer = RoadRestorationActivitySerializer(get_rr, many=False)                
            activity_info['task_id']=task_id
            activity_info['task_type'] = task_type
            activity_info['activity'] =serializer.data    
            return Response(activity_info)
            #break

        if task_type == "HSC":
            get_hsc = HSCActivity.objects.get(activity_id=activity_id)
            serializer = HSCActivitySerializer(get_hsc, many=False)                
            activity_info['task_id']=task_id
            activity_info['task_type'] = task_type
            activity_info['activity'] =serializer.data    
            return Response(activity_info)
            #break
        if task_type == "HK":
            get_hk = HKActivity.objects.get(activity_id=activity_id)
            serializer = HKActivitySerializer(get_hk, many=False)                
            activity_info['task_id']=task_id
            activity_info['task_type'] = task_type
            activity_info['activity'] =serializer.data    
            return Response(activity_info)
            #break            
        else:
            return Response("Incorrect task_type, please select a correct task_type")     
    else :
        return Response("Error")            

# Update the activity of a task.        

@api_view(["POST"])
def update_task_activity(request):
    if request.method=='POST':
        username = request.data['username']
        user = User.objects.get(username=username)                
        plan_id= request.data['plan_id'] 
        project_id = request.data['project_id'] 
        organization_id = request.data['organization_id'] 
        task_id = request.data['task_id']  
        activity_id = request.data['activity_id']         
        task_startnode = request.data['task_startnode']                 
        task_endnode = request.data['task_endnode']                         
        tasks = Task.objects.filter(task_project_id=project_id, task_organization_id = organization_id ,
         task_plan_id = plan_id, task_id =task_id)
        if tasks.count()>0:             
            if task_type == "CC":
                task_id = task_id
                update_cc = CCBreakingActivity.objects.get(task_id=task_id)
                update_cc.status=request.data['status'] 
                update_cc.completed_on=request.data['completed_on'] 
                updated_activity = update_cc.save()
                serializer = CCBreakingActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['plan'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
                
            if task_type == "Pipe":
                task_id = task_id                
                update_pipe = PipeLineActivity.objects.get(task_id=task_id)
                update_pipe.status=request.data['status'] 
                update_pipe.completed_on=request.data['completed_on'] 
                updated_activity = update_pipe.save()
                serializer = PipeLineActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['pipe'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "MH":
                task_id = task_id                
                update_mh = ManholeActivity.objects.get(task_id=task_id)
                update_mh.status=request.data['status'] 
                update_mh.completed_on=request.data['completed_on'] 
                updated_activity = update_mh.save()
                serializer = ManholeActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['Manhole'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "RR":
                task_id = task_id                
                update_rr = RoadRestorationActivity.objects.get(task_id=task_id)
                update_rr.status=request.data['status'] 
                update_rr.completed_on=request.data['completed_on'] 
                updated_activity = update_rr.save()
                serializer = RoadRestorationActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['RR'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "HSC":
                task_id = task_id                
                update_hsc = HSCActivity.objects.get(task_id=task_id)
                update_hsc.status=request.data['status'] 
                update_hsc.completed_on=request.data['completed_on'] 
                updated_activity = update_pipe.save()
                serializer = HSCActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['HSC'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
            if task_type == "HK":
                task_id = task_id,                                
                update_hk = HSCActivity.objects.get(task_id=task_id)
                update_hk.status=request.data['status'] 
                update_hk.completed_on=request.data['completed_on'] 
                updated_activity = update_hk.save()
                serializer = HSCActivitySerializer(updated_activity, many=False)                
                activity_result={}
                activity_result['HSC'] = serializer.data
                activity_result['isSuccessful']=True 
                activity_result['user'] =username
                activity_result['userRole'] ="Admin"
                activity_result['message'] ="Success"                          
                return Response(activity_result)
                #break
    else:
        return Response("Error")   