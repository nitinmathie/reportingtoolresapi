from rest_framework import serializers
from superrestapp.models import *
from superrestapp.serializers import *
class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = '__all__'
     
class OrganizationSerializer(serializers.ModelSerializer):     
    organization_users = UserSerializer(many=True, read_only = True)
    class Meta:
        model = Organization        
        fields = (
             'organization_id',
          'organization_name',
          'organization_email',
          'organization_address',
          'organization_logo' ,
          'organization_created_by' ,
          'organization_updated_by' ,
          'organization_created_on' ,
          'organization_updated_on' ,
           'organization_status',
           'organization_users'          
        )
      
   
        
class ProjectSerializer(serializers.ModelSerializer): 
    project_users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Project
        fields = (
            'project_id',
    'project_name',
    'organization_project_id',
    'project_type',
    'project_location',
    'project_status',
    'project_description',
    'project_created_by',
    'project_updated_by',
    'project_created_on',
    'project_updated_on',
    'project_users'
        )
        
class StoreSerializer(serializers.ModelSerializer): 
    store_users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Store
        fields = (
            'store_id',
    'store_name',
    'store_organization_id', 
    'store_project_id',
    'store_location',
    'created_on',
    'store_created_by',
    'updated_on',
    'store_updated_by',
    'store_users'

        )

class UserProjectRoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User_Role
        fields = '__all__'
class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'
