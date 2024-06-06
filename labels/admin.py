from django.contrib import admin
from .models import Label


# Register your models here.
class MyLabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'labelname', 'time_create')
    list_display_links = ('id', 'labelname')
    search_fields = ('labelname', 'id')
    list_filter = ['time_create']


admin.site.register(Label, MyLabelAdmin)
