#!/usr/bin/env python3

from django import forms
from statuses.models import Status


class NewStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['statusname']

    def save(self):
        self.clean()
        status = self.Meta.model(statusname=self.cleaned_data['statusname'])
        status.save()
        return status


class StatusDeleteForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = []
