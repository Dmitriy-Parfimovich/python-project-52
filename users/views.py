#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from users.models import User
from users.forms import UserRegForm, UserDeleteForm
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
        if request.user.is_authenticated:
            user = User.objects.get(pk=self.kwargs['pk'])
            form = UserRegForm(instance=user)
            if request.user == user:
                return render(request, 'users/reg.html', context={'form': form, 'user': user})
            else:
                messages.error(request, 'У вас нет прав для изменения другого пользователя.')
                return redirect('users_list')
        else:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect('users_list')
        return render(request, 'users/reg.html', context={'form': form})


class UserDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            delete_form = UserDeleteForm()
            user = User.objects.get(pk=self.kwargs['pk'])
            if request.user == user:
                return render(request, 'users/delete.html',
                              context={'form': delete_form, 'user': user})
            else:
                messages.error(request, 'У вас нет прав для изменения другого пользователя.')
                return redirect('users_list')
        else:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect('users_list')
