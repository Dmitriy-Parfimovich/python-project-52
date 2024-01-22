#!/usr/bin/env python3

import re
from django import forms
from django.contrib.auth import get_user_model
from users.models import User


class UserRegForm(forms.ModelForm):

    password2 = forms.CharField(max_length=20)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password', 'password2']

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
            self.errors['username'] = 'Введите правильное имя пользователя.\
                                       Оно может содержать только буквы, цифры и знаки @/./+/-/_.'
        elif User.objects.filter(username=self['username'].value()).exists():
            self.errors['username'] = 'Пользователь с таким именем уже существует.'
        return self['username'].value()

    def clean_password(self):
        if self['password'].value() != self['password2'].value():
            self.errors['password'] = 'Введенные пароли не совпадают.'
        elif len(self['password'].value()) <= 2:
            self.errors['password'] = 'Введённый пароль слишком короткий.\
                                        Он должен содержать как минимум 3 символа.'
        return self['password'].value()


class UserDeleteForm(forms.ModelForm):

    class Meta:
        model = User
        fields = []
