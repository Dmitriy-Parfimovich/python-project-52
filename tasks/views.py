from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
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

    """form_class = NewTaskForm
    queryset = Task.objects.all()
    object = None
    object_list = None
    template_name = 'tasks/tasks.html'
    filterset_class = TaskFilter

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, pk=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET:
            context['request_GET'] = True
            if 'self_tasks' in request.GET:
                taskautor = f'{request.user.first_name} {request.user.last_name}'
                self.queryset = self.queryset.filter(taskautor=taskautor)
                context['self_tasks'] = True
        myFilter = TaskFilter(request.GET, queryset=self.queryset)
        tasks = myFilter.qs.order_by('pk')
        context['form'] = myFilter.form
        context['tasks'] = tasks
        return render(request, self.template_name, context)"""


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

    def form_valid(self, form):
        task = form.instance
        taskautor = f'{self.request.user.first_name} {self.request.user.last_name}'
        task.taskautor = taskautor
        form.save()
        return super().form_valid(form)


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

    """def form_valid(self, form):
        task = form.instance
        if Task.objects.filter(name=task.name).exists():
            task_to_edit_from_form = Task.objects.get(name=task.name)
            if self.get_object() != task_to_edit_from_form.name:
                self.context['task_error'] = True
        else:
            task.save()
            labels = form.cleaned_data['labels']
            task.labels.set(labels)
        return super().form_valid(form)"""


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
