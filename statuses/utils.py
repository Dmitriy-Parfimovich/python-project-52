from statuses.models import Status
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _


class StatusDataMixin():

    model = Status

    def mixin_dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')
