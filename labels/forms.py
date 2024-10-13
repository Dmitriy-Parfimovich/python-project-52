import re
from django import forms
from labels.models import Label
from django.utils.translation import gettext as _


class NewLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']

    def clean_name(self):
        if re.search(r"^\s*$", self['name'].value()):
            self.errors['name'] = _('Required field.')
        return self['name'].value().strip()


"""class LabelDeleteForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = []"""
