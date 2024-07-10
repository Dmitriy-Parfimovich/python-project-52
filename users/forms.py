import re
from django import forms
from django.contrib.auth import get_user_model
from users.models import User
from django.utils.translation import gettext as _


class UserRegForm(forms.ModelForm):

    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def save(self):
        self.clean()
        user = self.Meta.model(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()
        return user

    def clean_username(self):
        if re.search(r'[^\w\-@.+]', self['username'].value()):
            self.errors['username'] = _('Please enter a correct username.\
                                        It can only contain letters,\
                                        numbers and symbols @/./+/-/_.')
        elif User.objects.filter(username=self['username'].value()).exists():
            self.errors['username'] = _('A user with the same name already exists.')
        return self['username'].value()

    def clean_password1(self):
        if self['password1'].value() != self['password2'].value():
            self.errors['password1'] = _('Entered passwords do not match')
        elif len(self['password1'].value()) <= 2:
            self.errors['password1'] = _('The entered password is too short.\
                                        It must contain at least 3 characters.')
        return self['password2'].value()


class UserDeleteForm(forms.ModelForm):

    class Meta:
        model = User
        fields = []
