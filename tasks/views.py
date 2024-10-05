from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView,
                                  UpdateView,
                                  DeleteView)
from tasks.models import Task
from labels.models import Label
from tasks.forms import NewTaskForm, TaskDeleteForm
from django.utils.translation import gettext as _
from .filters import TaskFilter
from django_filters.views import FilterView
from tasks.utils import TaskDataMixin
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class TasksListView(TaskDataMixin, FilterView):

    filterset_class = TaskFilter
    template_name = 'tasks/tasks.html'
    object = None
    context_object_name = 'tasks'
    filterset_fields = ['executor', 'status', 'labels']


class NewTaskView(SuccessMessageMixin, TaskDataMixin, CreateView):

    form_class = NewTaskForm
    template_name = 'tasks/new_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task created successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, pk=None)

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, pk=None)

    """def form_valid(self, form):
        task = form.instance
        taskautor = f'{self.request.user.first_name} {self.request.user.last_name}'
        task.taskautor = taskautor
        form.save()
        return super().form_valid(form)"""


class TaskEditView(SuccessMessageMixin, TaskDataMixin, UpdateView):

    form_class = NewTaskForm
    object = None
    template_name = 'tasks/new_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task was successfully modified')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, pk=self.kwargs['pk'])


class TaskDeleteView(SuccessMessageMixin, TaskDataMixin, DeleteView):

    form_class = TaskDeleteForm
    template_name = 'tasks/del_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task was successfully deleted')

    def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)


class TaskInfoView(View):

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        labels = Label.objects.filter(task__name=task.name)
        return render(request, 'tasks/task_info.html', context={'task': task,
                                                                'labels': labels})
