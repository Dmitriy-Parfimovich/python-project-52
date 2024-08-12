from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from users.models import User
from tasks.models import Task
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from users.forms import UserRegForm, UserDeleteForm
from django.utils.translation import gettext as _
from users.utils import UserDataMixin


# Create your views here.
class UsersListView(ListView):
    queryset = User.objects.all().order_by('pk')
    context_object_name = 'users'
    template_name = 'users/users.html'


class NewUserRegView(UserDataMixin, CreateView):

    form_class = UserRegForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('login')

    """def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['user_is_auth'] = False
        if self.request.user.is_authenticated:
            context['user_is_auth'] = True
        return context"""
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, pk=None)
    
    def form_valid(self, form):
        user = form.instance
        user.save()
        user.set_password(form.cleaned_data['password2'])
        messages.success(self.request, _('User successfully registered'))
        return super().form_valid(form)


class UserEditView(UserDataMixin, UpdateView):

    #model = User
    form_class = UserRegForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('users_list')

    """def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])"""

    """def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.request.user != self.get_object():
                messages.error(request, _('You do not have permission to change\
                                          another user.'))
                return redirect('users_list')
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')"""
    
    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    """def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        if self.request.user == self.get_object():
            context['user'] = self.get_object()
        return context"""
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, pk=self.kwargs['pk'])

    def form_valid(self, form):
        tasks_of_old_user = Task.objects.filter(taskautor=self.get_object())
        for task in tasks_of_old_user:
                task.taskautor = self.get_object()
                task.save()
        user = self.get_object()
        user = form.instance
        user.save()
        messages.success(self.request, _('User successfully changed'))
        return super().form_valid(form)


class UserDeleteView(UserDataMixin, DeleteView):

    # model = User
    form_class = UserDeleteForm
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')

    """def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])"""
    
    """def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user == self.get_object():
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, _('You do not have permission\
                                          to change another user.'))
                return redirect('users_list')
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')"""
    
    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if Task.objects.filter(executor__username=user.username).exists():
            messages.error(request, _('Cannot delete user because it is in use'))
        else:
            user.delete()
            messages.success(request, _('User deleted successfully'))
        return redirect('users_list')
