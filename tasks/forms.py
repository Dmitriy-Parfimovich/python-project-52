# import re
from django import forms
from tasks.models import Task
# from django.utils.translation import gettext as _


class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
