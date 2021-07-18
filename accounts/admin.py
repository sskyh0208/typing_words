from .models import Users
from django.contrib import admin


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_superuser', 'last_login']

# Register your models here.
admin.site.register(Users, UsersAdmin)