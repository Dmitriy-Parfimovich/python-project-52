#!/usr/bin/env python3

from django import forms
from tasks.models import Task


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
        return self['taskname'].value()


class TaskDeleteForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = []
