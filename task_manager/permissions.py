from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib import messages


class LoginRequiredMixinWithMessage(LoginRequiredMixin):
    
    login_url = reverse_lazy('login')
    login_required_message = _('You are not authorized! Please log in.')

    def mixin_dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, self.login_required_message)
            return reverse_lazy('login')
        if request.user != self.get_object():
            messages.error(request, _('You do not have permission to change\
                                       another user.'))
            return redirect('users_list')
        #return super().dispatch(request, *args, **kwargs)
