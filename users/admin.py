from django.contrib import admin
from .models import User


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'password', 'time_create')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'id')
    list_filter = ['time_create']


admin.site.register(User, MyUserAdmin)
