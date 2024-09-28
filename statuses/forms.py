import re
from django import forms
from statuses.models import Status
from django.utils.translation import gettext as _


class NewStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        if re.search(r"^\s*$", self['name'].value()):
            self.errors['name'] = _('Required field.')
        return self['name'].value().strip()


class StatusDeleteForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = []
