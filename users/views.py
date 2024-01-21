#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from users.models import User
from users.forms import UserRegForm
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by('pk')
        return render(request, 'users/users.html', context={'users': users})


class NewUserRegView(View):

    def get(self, request, *args, **kwargs):
        form = UserRegForm()
        return render(request, 'users/reg.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('login')
        return render(request, 'users/reg.html', context={'form': form})


class LoginUserView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Вы залогинены')
        return reverse_lazy('home')

    def form_invalid(self, form):
        form.add_error(None, 'Пожалуйста, введите правильные имя пользователя и пароль.\
                              Оба поля могут быть чувствительны к регистру.')
        return self.render_to_response(self.get_context_data(form=form))


class LoginOutView(LogoutView):

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Вы разлогинены')
        return reverse_lazy('home')


class UserEditView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/edit.html', context={'title': 'Изменение пользователя'})


class UserDeleteView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/delete.html', context={'title': 'Удаление пользователя'})
