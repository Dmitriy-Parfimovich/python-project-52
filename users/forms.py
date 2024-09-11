import re
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from users.models import User
from django.utils.translation import gettext as _


class UserRegForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserDeleteForm(forms.ModelForm):

    class Meta:
        model = User
        fields = []
