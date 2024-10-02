from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'task_manager/index.html')


class LoginUserView(SuccessMessageMixin, LoginView):

    template_name = 'users/login.html'
    success_message = _('You are logged in')
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        # messages.add_message(self.request, messages.SUCCESS, _('You are logged in'))
        return reverse_lazy('home')


class LoginOutView(LogoutView):

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('You are logged out'))
        return reverse_lazy('home')
