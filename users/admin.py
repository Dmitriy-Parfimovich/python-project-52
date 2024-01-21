from django.contrib import admin
from .models import User


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'password', 'time_create')


admin.site.register(User, MyUserAdmin)
