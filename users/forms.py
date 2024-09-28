from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User


class UserRegForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserDeleteForm(forms.ModelForm):

    class Meta:
        model = User
        fields = []
