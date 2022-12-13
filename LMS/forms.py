from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .models import CustomUser
from django import forms

 
class LoginForm(forms.Form):
    Ticket_No = forms.IntegerField(
        widget = forms.NumberInput(
            attrs = {
                "class" : "form-control",
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class" : "form-control",
            }
        )
    
    )

class UserShopAddForm(UserCreationForm):
	'''
	Extending UserCreationForm - with email

	'''

	class Meta:
		model = CustomUser
		fields = ['Ticket_No','Complete_Name','password1','password2','Cost_Center_Name','is_active']
		

class UserSuperAddForm(UserCreationForm):
	'''
	Extending UserCreationForm - with email

	'''

	class Meta:
		model = CustomUser
		fields = ['Ticket_No','Complete_Name','password1','password2','is_active']
		
	

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('Ticket_No',)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('Ticket_No',)