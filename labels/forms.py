#!/usr/bin/env python3

from django import forms
from labels.models import Label


class NewLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['labelname']

    def save(self):
        self.clean()
        label = self.Meta.model(labelname=self.cleaned_data['labelname'])
        label.save()
        return label


class LabelDeleteForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = []
