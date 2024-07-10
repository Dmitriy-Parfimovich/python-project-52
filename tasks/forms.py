import re
from django import forms
from tasks.models import Task
from django.utils.translation import gettext as _


class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def save(self):
        self.clean()
        task = self.Meta.model(name=self.cleaned_data['name'],
                               description=self.cleaned_data['description'],
                               status=self.cleaned_data['status'],
                               executor=self.cleaned_data['executor'],
                               taskautor=self.cleaned_data['taskautor'],
                               )
        task.save()
        labels = self.cleaned_data['labels']
        task.labels.set(labels)
        return task

    def clean_name(self):
        if re.search(r"^\s*$", self['name'].value()):
            self.errors['name'] = _('Required field.')
        return self['name'].value().strip()


class TaskDeleteForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = []
