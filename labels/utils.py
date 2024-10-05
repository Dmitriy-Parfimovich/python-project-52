from labels.models import Label
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _


class Mixins():

    model = Label

    def mixin_dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')
