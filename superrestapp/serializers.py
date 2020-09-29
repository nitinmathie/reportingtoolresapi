from rest_framework import serializers
from superrestapp.models import *
from superrestapp.serializers import *
class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = '__all__'
        
class OrganizationSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Organization
        fields = '__all__'
      
        
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
