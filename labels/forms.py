#!/usr/bin/env python3

import re
from django import forms
from labels.models import Label
from django.utils.translation import gettext as _


class NewLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']

    def save(self):
        self.clean()
        label = self.Meta.model(name=self.cleaned_data['name'])
        label.save()
        return label

    def clean_name(self):
        if re.search(r"^\s*$", self['name'].value()):
            self.errors['name'] = _('Required field.')
        return self['name'].value().strip()


class LabelDeleteForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = []
