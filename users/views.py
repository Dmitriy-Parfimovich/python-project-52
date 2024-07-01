#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from users.models import User
from tasks.models import Task
from users.forms import UserRegForm, UserDeleteForm
from django.utils.translation import gettext as _


# Create your views here.
class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by('pk')
        return render(request, 'users/users.html', context={'users': users})


class NewUserRegView(View):

    def get(self, request, *args, **kwargs):
        form = UserRegForm()
        user_is_auth = False
        if request.user.is_authenticated:
            user_is_auth = True
        return render(request, 'users/reg.html', context={'form': form,
                                                          'user_is_auth': user_is_auth})

    def post(self, request, *args, **kwargs):
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully registered'))
            return redirect('login')
        return render(request, 'users/reg.html', context={'form': form})


class UserEditView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(pk=self.kwargs['pk'])
            form = UserRegForm(instance=user)
            if request.user == user:
                return render(request, 'users/reg.html', context={'form': form, 'user': user})
            else:
                messages.error(request, _('You do not have permission to change\
                                          another user.'))
                return redirect('users_list')
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=self.kwargs['pk'])
            tasks_of_old_user = Task.objects.filter(taskautor=user.username)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            for task in tasks_of_old_user:
                task.taskautor = user.username
                task.save()
            messages.success(request, _('User successfully changed'))
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
                messages.error(request, _('You do not have permission\
                                          to change another user.'))
                return redirect('users_list')
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')

    def post(self, request, *args, **kwargs):
        user = request.user
        if Task.objects.filter(executor__username=user.username).exists():
            messages.error(request, _('Cannot delete user because it is in use'))
        else:
            user.delete()
            messages.success(request, _('User deleted successfully'))
        return redirect('users_list')
