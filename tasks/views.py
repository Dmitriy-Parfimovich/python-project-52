from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  UpdateView,
                                  DeleteView)
from tasks.models import Task
from tasks.forms import NewTaskForm
from django.utils.translation import gettext as _
from .filters import TaskFilter
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.permissions import LoginRequiredMixinWithMessage
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.detail import DetailView


# Create your views here.
class TasksListView(LoginRequiredMixinWithMessage, FilterView):

    filterset_class = TaskFilter
    template_name = 'tasks/tasks.html'
    object = None
    context_object_name = 'tasks'
    filterset_fields = ['executor', 'status', 'labels']


class NewTaskView(LoginRequiredMixinWithMessage, SuccessMessageMixin, CreateView):

    form_class = NewTaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task created successfully')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskEditView(LoginRequiredMixinWithMessage, SuccessMessageMixin, UpdateView):

    model = Task
    form_class = NewTaskForm
    object = None
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task was successfully modified')


class TaskDeleteView(LoginRequiredMixinWithMessage, SuccessMessageMixin, DeleteView):

    model = Task
    template_name = 'tasks/del_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task was successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task_author = Task.objects.get(id=task_id).author
        if request.user == task_author:
            return super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.ERROR, _("Only it's author can delete the task"))
        return redirect(reverse_lazy('tasks_list'))


class TaskInfoView(LoginRequiredMixinWithMessage, DetailView):

    model = Task
    template_name = 'tasks/task_info.html'
    login_url = reverse_lazy('login')
    context_object_name = 'task'
