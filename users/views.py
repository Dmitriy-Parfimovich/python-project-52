from django.urls import reverse_lazy
from django.contrib import messages
from users.models import User
from tasks.models import Task
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from users.forms import UserRegForm, UserDeleteForm
from django.utils.translation import gettext as _
from users.utils import UserDataMixin
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class UsersListView(ListView):

    queryset = User.objects.all().order_by('pk')
    context_object_name = 'users'
    template_name = 'users/users.html'


class NewUserRegView(SuccessMessageMixin, CreateView):

    form_class = UserRegForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')

    def form_valid(self, form):
        user = form.instance
        user.save()
        user.set_password(form.cleaned_data['password2'])
        return super().form_valid(form)


class UserEditView(SuccessMessageMixin, UserDataMixin, UpdateView):

    form_class = UserRegForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully changed')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, pk=self.kwargs['pk'])

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
        return super().form_valid(form)


class UserDeleteView(SuccessMessageMixin, UserDataMixin, DeleteView):

    form_class = UserDeleteForm
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User deleted successfully')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, pk=self.kwargs['pk'])

    def form_valid(self, form):
        user = self.get_object()
        if Task.objects.filter(executor__username=user).exists():
            messages.error(self.request, _('Cannot delete user because it is in use'))
        else:
            user.delete()
        return super().form_valid(form)
