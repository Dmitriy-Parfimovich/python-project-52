#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from users.models import User
from users.forms import UserRegForm, UserDeleteForm
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext as _


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
            messages.success(request, _('Usersuccessfullyregistered'))
            return redirect('login')
        return render(request, 'users/reg.html', context={'form': form})


class LoginUserView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, _('Youareloggedin'))
        return reverse_lazy('home')

    def form_invalid(self, form):
        form.add_error(None, _('Bothfieldscanbecasesensitive'))
        return self.render_to_response(self.get_context_data(form=form))


class LoginOutView(LogoutView):

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Youareloggedout'))
        return reverse_lazy('home')


class UserEditView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(pk=self.kwargs['pk'])
            form = UserRegForm(instance=user)
            if request.user == user:
                return render(request, 'users/reg.html', context={'form': form, 'user': user})
            else:
                messages.error(request, _('Nothavepermission'))
                return redirect('users_list')
        else:
            messages.error(request, _('Notauthorized'))
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=self.kwargs['pk'])
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, _('Usersuccessfullychanged'))
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
                messages.error(request, _('Notchangeanotheruser'))
                return redirect('users_list')
        else:
            messages.error(request, _('Notauthorizedplease'))
            return redirect('login')

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        messages.success(request, _('Deletedsuccessfully'))
        return redirect('users_list')
