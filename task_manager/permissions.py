from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib import messages


class LoginRequiredMixinWithMessage(LoginRequiredMixin):
    
    login_url = reverse_lazy('login')
    login_required_message = _('You are not authorized! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, self.login_required_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserTestPassesMixinWithMessage(UserPassesTestMixin):

    message = _("You don't have permission to change another user.")
    permission_denied_message = message
    
    def test_func(self):
        return self.request.user.id == self.kwargs.get("pk")

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            messages.add_message(request, messages.ERROR, self.permission_denied_message)
            return redirect(reverse_lazy('users_list'))
        return super().dispatch(request, *args, **kwargs)
