from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
#    blog/admin.py

class UserAdmin(admin.ModelAdmin):
    list_display = ('bio', 'profile_image', 'location')
    
admin.site.register(User, UserAdmin)

