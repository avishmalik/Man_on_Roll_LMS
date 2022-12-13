from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser,PermissionsMixin
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
from .manager import CustomUserManager 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractBaseUser,PermissionsMixin):
    last_login = None
    # groups = None
    # user_permissions = None
    # id = models.AutoField(primary_key=True)
    # username = None
    Ticket_No = models.IntegerField(_('Ticket_No'),unique=True)
    Complete_Name= models.CharField(max_length = 100)
    Current_Shop = models.CharField(max_length = 100)
    Cost_Center_Name = models.CharField(max_length = 100)
    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= False)
    is_mor = models.BooleanField(default = True)
    is_supervisor = models.BooleanField(default = False)
    is_shop_incharge = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'Ticket_No'
    REQUIRED_FIELDS = ['Complete_Name','Current_Shop','Cost_Center_Name','is_mor','is_supervisor','is_shop_incharge']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return str(self.Ticket_No)

# class Person(models.Model):
#     id = models.AutoField(primary_key=True)
#     Ticket_No = models.IntegerField(unique = True,null = False)
#     Complete_Name= models.CharField(max_length = 100)
#     Current_Shop = models.CharField(max_length = 100)
#     Cost_Center_Name = models.CharField(max_length =100)
#     password = models.CharField(max_length = 100,default='tatamotors')
    
#     class Meta: 
#         verbose_name = 'Person'
#         verbose_name_plural = 'Persons'
    
#     def __str__(self):
#         return self.Complete_Name  
    

# class SuperV(models.Model):
#     Ticket_No = models.IntegerField(primary_key = True,null= False)
#     Complete_Name= models.CharField(max_length = 100)
#     Current_Shop = models.CharField(max_length = 100)
#     Cost_Center_Name = models.CharField(max_length =100)
#     password = models.CharField(max_length = 100,default='tatamotors')

#     class Meta: 
#         verbose_name = 'Supervisor'
#         verbose_name_plural = 'Supervisors'
        
#     def __str__(self):
#         return self.Complete_Name
    

