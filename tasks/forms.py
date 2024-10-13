import re
from django import forms
from tasks.models import Task
from django.utils.translation import gettext as _


class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def clean_name(self):
        if re.search(r"^\s*$", self['name'].value()):
            self.errors['name'] = _('Required field.')
        return self['name'].value().strip()


"""class TaskDeleteForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = []"""
