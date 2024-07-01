from django.contrib import admin
from .models import Label


# Register your models here.
class MyLabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'id')
    list_filter = ['time_create']


admin.site.register(Label, MyLabelAdmin)
