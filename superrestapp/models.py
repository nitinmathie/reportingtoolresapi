from django.db import models
from django.core.validators import MinLengthValidator

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True, validators=[MinLengthValidator(5)])
    user_email = models.EmailField(max_length=254, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True, validators=[MinLengthValidator(8)])

class User_Profile(models.Model):
    user_profile_id = models.AutoField(primary_key =True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300)
    address_proof = models.ImageField()
    date_of_birth = models.DateField()
    created_on = models.DateField()
    created_by = models.ForeignKey('self', on_delete =models.CASCADE, related_name = 'profile_created_by')
    updated_by = models.ForeignKey('self', on_delete =models.CASCADE, related_name = 'profile_updated_by')
    updated_on = models.DateField()
    profile_completed_status = models.BooleanField(default=False)
                
class Organization(models.Model):
    organization_id=models.AutoField(primary_key=True, null =False)
    organization_name=models.CharField(max_length=100, null=True, blank=True)
    organization_email=models.EmailField(max_length=254, null=True, blank=True)
class Organization_Profile(models.Model):
    organization_profile_id = models.IntegerField(primary_key =True)
    organization= models.OneToOneField(Organization, on_delete=models.CASCADE)
    organization_address= models.CharField(max_length=100, null=True, blank=True)
    organization_logo = models.ImageField()
    organization_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='created_by')
    organization_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='updated_by')
    organization_created_on = models.DateField()
    organization_updated_on = models.DateField()
    organization_status=models.BooleanField(default=False)
    organization_users = models.ManyToManyField(User)
class Project(models.Model):
    project_id=models.AutoField(primary_key=True)
    project_name=models.CharField(max_length=100, null=True, blank=True)
    organization_project_id=models.ForeignKey(Organization, on_delete=models.CASCADE)
class Project_Profile(models.Model):
    project_profile_id = models.AutoField(primary_key =True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    project_type = models.CharField(max_length=100, null=True, blank=True) # choices field with all the construction fields available    
    project_location = models.CharField(max_length=100, null=True, blank=True)
    project_status = models.BooleanField(default=False)
    project_description = models.CharField(max_length=100, null=True, blank=True)
    project_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='project_created_by')
    project_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_updated_by')
    project_created_on = models.DateField()
    project_updated_on = models.DateField()
    project_users = models.ManyToManyField(User)
class User_Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, null=True, blank=True)
class Users_Projects(models.Model):
    pass
class Organization_Projects(models.Model):
    pass
class Project_Plan(models.Model):
    plan_id=models.AutoField(primary_key=True)
    project_id=models.ForeignKey(Project, on_delete=models.CASCADE)
    plan_description = models.CharField(max_length=100, null=True, blank=True)
    plan_file = models.ImageField()   
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_detail = models.CharField(max_length=100, null=True, blank=True)
    plan_id = models.ForeignKey(Project_Plan, on_delete=models.CASCADE)
    from_node = models.CharField(max_length=100, null=True, blank=True)
    to_node = models.CharField(max_length=100, null=True, blank=True)
    length = models.CharField(max_length=100, null=True, blank=True)
    breadth = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=100, null=True, blank=True)
    task_created_on = models.DateField()
    task_created_by = models.ForeignKey(User,on_delete=models.CASCADE)
class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_on = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    material_name = models.CharField(max_length=100, null=True, blank=True)
    type_of_material = models.CharField(max_length=100, null=True, blank=True) #Choices
    material_image = models.ImageField()
    unit_price = models.FloatField()
    description = models.CharField(max_length=100, null=True, blank=True)    
class Task_Assignment(models.Model):
    task_id = models.OneToOneField(Task,on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'assigned_by')
    assigned_on = models.DateField()
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE, related_name ='assigned_to' )
class Task_Report(models.Model):
    task_id = models.OneToOneField(Task,on_delete=models.CASCADE)
    manpower = models.FloatField()
    machinary = models.CharField(max_length=100, null=True, blank=True)
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE)
    reported_at = models.DateField()
    taskcompletion_images = models.ImageField
    material_used = models.CharField(max_length=100, null=True, blank=True)
class Indent_Request(models.Model):
    required_material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    number_of_units = models.IntegerField()
    task_id= models.ForeignKey(Task, on_delete=models.CASCADE)
    

class Materials_Indent(models.Model):
    user_id= models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_user_id')
    materials = models.ManyToManyField(Indent_Request)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_by')
    requested_at = models.DateField()
    requested_to = models.ForeignKey(Store, on_delete=models.CASCADE)
    received =models.BooleanField(default=False)   
class Indent_Response_To_User(models.Model):
    requested_material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    number_of_units = models.IntegerField()
    received_from = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_from')
    received_at = models.DateField()
    dispatched_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_to')
    dispatched_at = models.DateField()
  
class Otp(models.Model):
    email = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField()
