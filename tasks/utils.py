from tasks.models import Task
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _


class TaskDataMixin(SingleObjectMixin):

    model = Task
    
    """def get_mixin_context(self, context, **kwargs):
        context['user_is_auth'] = False
        if kwargs['pk'] and self.request.user == self.get_object():
                context['user'] = self.get_object()
        elif self.request.user.is_authenticated:
            context['user_is_auth'] = True
        return context"""
    
    def mixin_dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.get_object().taskautor != f'{request.user.first_name} {request.user.last_name}':
                messages.error(request, _("Only it's author can delete the task"))
                return redirect('tasks_list')
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')
    
    """def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.get_object().taskautor == f'{request.user.first_name} {request.user.last_name}':
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, _("Only it's author can delete the task"))
                return redirect('tasks_list')
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')"""
