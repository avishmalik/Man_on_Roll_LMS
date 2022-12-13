
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# from .models import Person,SuperV
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin,ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('Ticket_No','is_staff','Complete_Name','Current_Shop','Cost_Center_Name','is_mor','is_supervisor','is_shop_incharge')
    list_filter = ('Ticket_No','is_staff','Complete_Name','Current_Shop','Cost_Center_Name','is_mor','is_supervisor','is_shop_incharge')
    fieldsets = (
        (None,{'fields': ('Ticket_No','password','Complete_Name','Current_Shop','Cost_Center_Name','is_mor','is_supervisor','is_shop_incharge')}),
        ('Permissions', {'fields': ('is_staff','is_active',)}),
    )
    
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields' : ('Ticket_No','password1','password2','is_staff','is_active','Complete_Name','Current_Shop','Cost_Center_Name','is_mor','is_supervisor','is_shop_incharge')}
        ),
    )
    search_fields = ('Ticket_No','Complete_Name')
    ordering = ('Ticket_No',)




# admin.site.register(CustomUser,CustomUserAdmin)

# class UserResource(resources.ModelResource):
#     class Meta:
#         model = CustomUser
#         # fields = ('id','Ticket_No','Complete_Name','Current_Shop','Cost_Center_Name')
#         list_display = ('id','Ticket_No','Complete_Name','Current_Shop','Cost_Center_Name')

# class UserAdmin(ImportExportModelAdmin,UserAdmin):
#     resource_class = UserResource
#     pass

# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)


# class PersonResource(resources.ModelResource):

#     class Meta:
#         model = Person

# class PersonAdmin(ImportExportModelAdmin):
#     list_display = ('id','Ticket_No','Complete_Name','Current_Shop','Cost_Center_Name')
#     resource_class = PersonResource

# admin.site.register(Person, PersonAdmin)

# class SuperVAdmin(admin.ModelAdmin):
#     list_display = ('Ticket_No','Complete_Name','Current_Shop','Cost_Center_Name')
    
# admin.site.register(SuperV,SuperVAdmin)






