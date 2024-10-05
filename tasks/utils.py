from tasks.models import Task
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _


class Mixins(SingleObjectMixin):

    model = Task

    def get_mixin_context(self, context, **kwargs):
        if kwargs['pk']:
            context['edit_flag'] = True
        return context

    def mixin_dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if kwargs['pk'] and self.get_object().taskautor != request.user.get_full_name():
                messages.error(request, _("Only it's author can delete the task"))
                return redirect('tasks_list')
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')
