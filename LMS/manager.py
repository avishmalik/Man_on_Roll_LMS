from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self,Ticket_No,password,**extra_fields):
        if not Ticket_No:
            raise ValueError(_('The Ticket No must be set'))
        # Ticket_No = self.normalize_ticket_no(Ticket_No)
        user = self.model(Ticket_No = Ticket_No,**extra_fields)
        user.set_password(raw_password = password)
        user.save()
        return user
    
    def create_superuser(self,Ticket_No,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('SuperUser must have is_staff True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('SuperUser must have is_superuser True'))
        return self.create_user(Ticket_No,password,**extra_fields)
        