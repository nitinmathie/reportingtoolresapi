from django.db import models
from django.core.validators import MinLengthValidator

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True, validators=[MinLengthValidator(5)])
    user_email = models.EmailField(max_length=254, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True, validators=[MinLengthValidator(8)])
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    address_proof = models.ImageField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_on = models.DateField(null=True, blank=True)
    #user_created_by = models.ForeignKey('self', on_delete =models.CASCADE, related_name = 'user_created_by_id')
    #user_updated_by = models.ForeignKey('self', on_delete =models.CASCADE, related_name = 'user_updated_by_id')
    updated_on = models.DateField(null=True, blank=True)
    profile_completed_status = models.BooleanField(default=False)                
class Organization(models.Model):
    organization_id=models.AutoField(primary_key=True)
    organization_name=models.CharField(max_length=100, null=True, blank=True)
    organization_email=models.CharField(max_length=254, null=True, blank=True)
    organization_address= models.CharField(max_length=100, null=True, blank=True)
    organization_logo = models.ImageField(null=True, blank=True)
    organization_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='created_by')
    organization_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='updated_by')
    organization_created_on = models.DateField(null=True, blank=True)
    organization_updated_on = models.DateField(null=True, blank=True)
    organization_status=models.BooleanField(default=False)
    organization_users = models.ManyToManyField(User,related_name='organization_users',blank=True)
class Project(models.Model):
    project_id=models.AutoField(primary_key=True)
    project_name=models.CharField(max_length=100, null=True, blank=True)
    organization_project_id=models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_project_id')
    project_type = models.CharField(max_length=100, null=True, blank=True)
    project_location = models.CharField(max_length=100, null=True, blank=True)
    project_status = models.BooleanField(default=False)
    project_description = models.CharField(max_length=100, null=True, blank=True)
    project_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='project_created_by')
    project_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_updated_by')
    project_created_on = models.DateField(null=True, blank=True)
    project_updated_on = models.DateField(null=True, blank=True)
    project_users = models.ManyToManyField(User,related_name='project_users',blank=True)

class User_Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, null=True, blank=True)
class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_organization_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='store_organization_id')
    store_project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='store_project_id')
    store_location= models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateField(null=True, blank=True)
    store_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_created_by')    
    updated_on = models.DateField(null=True, blank=True)
    store_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_updated_by')
    store_users= models.ManyToManyField(User,related_name='store_users',blank=True)

class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=100, null = True, blank = True)
    plan_description = models.CharField(max_length=100, null = True, blank = True)
    plan_template =  models.CharField(max_length=100, null = True, blank = True)
    plan_project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='plan_project_id')
    plan_organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='plan_organization_id')
    plan_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plan_created_by')
    plan_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plan_updated_by')

class Otp(models.Model):
    email = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField()
