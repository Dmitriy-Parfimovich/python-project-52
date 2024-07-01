#!/usr/bin/env python3

import re
from django import forms
from statuses.models import Status
from django.utils.translation import gettext as _


class NewStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['statusname']

    def save(self):
        self.clean()
        status = self.Meta.model(statusname=self.cleaned_data['statusname'])
        status.save()
        return status

    def clean_statusname(self):
        if re.search(r"^\s*$", self['statusname'].value()):
            self.errors['statusname'] = _('Required field.')
        return self['statusname'].value().strip()


class StatusDeleteForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = []
