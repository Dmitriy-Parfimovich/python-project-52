#!/usr/bin/env python3

import re
from django import forms
from tasks.models import Task
from django.utils.translation import gettext as _


class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['taskname', 'taskdescription', 'status', 'executor', 'label']

    def save(self):
        self.clean()
        task = self.Meta.model(taskname=self.cleaned_data['taskname'],
                               taskdescription=self.cleaned_data['taskdescription'],
                               status=self.cleaned_data['status'],
                               executor=self.cleaned_data['executor'],
                               taskautor=self.cleaned_data['taskautor'],
                               )
        task.save()
        labels = self.cleaned_data['label']
        task.label.set(labels)
        return task

    def clean_taskname(self):
        if re.search(r"^\s*$", self['taskname'].value()):
            self.errors['taskname'] = _('Required field.')
        return self['taskname'].value().strip()


class TaskDeleteForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = []
