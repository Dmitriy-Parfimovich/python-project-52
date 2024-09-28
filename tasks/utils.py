from tasks.models import Task
from users.models import User
from statuses.models import Status
from labels.models import Label
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _


class TaskDataMixin(SingleObjectMixin):

    model = Task

    def get_mixin_context(self, context, **kwargs):
        """context['statuses'] = Status.objects.all().order_by('pk')
        context['taskexecutors'] = User.objects.all().order_by('pk')
        context['labels'] = Label.objects.all().order_by('pk')
        context['request_GET'] = False
        context['self_tasks'] = False"""
        if kwargs['pk']:
            context['edit_flag'] = True
            """context['task_error'] = False"""
        return context

    def mixin_dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if kwargs['pk'] and \
               self.get_object().taskautor != f'{request.user.first_name} {request.user.last_name}':
                messages.error(request, _("Only it's author can delete the task"))
                return redirect('tasks_list')
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')
