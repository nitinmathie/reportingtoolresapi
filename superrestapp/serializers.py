from rest_framework import serializers
from superrestapp.models import *
from superrestapp.serializers import *
class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = '__all__'
        
class OrganizationSerializer(serializers.ModelSerializer): 
   # organization_created_by = UserSerializer(read_only=True, many=False)
   # organization_updated_by = UserSerializer(read_only=True, many=False)
    organization_users = UserSerializer(read_only=True, many=True)
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
    class Meta:
        model = Project
        fields = '__all__'
class UserProjectRoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User_Role
        fields = '__all__'
class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'
