#from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import path
from .views import (userregistration_view,  gensend_otp, verify_otp, userlogin_view,get_allusers, get_organizations_view,
add_organization_view, add_project_view, get_projects_view, add_store_view, get_stores_view, get_users_view,add_user_view,
add_task, assign_task_activity,fetch_plan_tasks, report_task_activity, fetch_task_activities, fetch_task_activity,
update_task_activity)

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
path('getplans',get_project_plans, name='getplans'),
path('addtask',add_task, name='addtask'),
path('gettask',fetch_plan_tasks, name='gettask'),
path('gettaskactivities',fetch_task_activities, name='gettaskactivities'),
path('getactivity',fetch_task_activity, name='getactivity'),
path('updatetaskactivity',update_task_activity, name='updatetaskactivity'),
path('assigntask',assign_task_activity, name='assigntask'),
path('reporttask',report_task_activity, name='reporttask'),
]



