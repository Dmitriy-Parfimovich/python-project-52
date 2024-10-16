from django.urls import reverse_lazy
from django.contrib import messages
from users.models import User
from tasks.models import Task
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from users.forms import UserRegForm
from django.utils.translation import gettext as _
from task_manager.permissions import LoginRequiredMixinWithMessage, UserTestPassesMixinWithMessage
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import MultipleObjectMixin


# Create your views here.
class UsersListView(ListView, MultipleObjectMixin):

    model = User
    ordering = 'pk'
    context_object_name = 'users'
    template_name = 'users/users.html'


class NewUserRegView(SuccessMessageMixin, CreateView):

    form_class = UserRegForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserEditView(LoginRequiredMixinWithMessage,
                   UserTestPassesMixinWithMessage,
                   SuccessMessageMixin,
                   UpdateView):

    model = User
    form_class = UserRegForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully changed')

    def form_valid(self, form):
        tasks_of_old_user = Task.objects.filter(author=self.get_object())
        for task in tasks_of_old_user:
            task.author = str(self.get_object())
            task.save()
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixinWithMessage,
                     UserTestPassesMixinWithMessage,
                     SuccessMessageMixin,
                     DeleteView):

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User deleted successfully')

    def form_valid(self, form):
        user = self.get_object()
        if Task.objects.filter(executor__username=user).exists():
            messages.error(self.request, _('Cannot delete user because it is in use'))
        return super().form_valid(form)
