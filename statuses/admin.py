from django.contrib import admin
from .models import Status


# Register your models here.
class MyStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'id')
    list_filter = ['time_create']


admin.site.register(Status, MyStatusAdmin)
