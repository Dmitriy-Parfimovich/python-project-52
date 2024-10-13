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
from tasks.utils import Mixins
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, pk=None)

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, pk=None)

    """def form_valid(self, form):
        task = form.instance
        task.author = self.request.user
        form.save()
        return super().form_valid(form)"""
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskEditView(LoginRequiredMixinWithMessage, SuccessMessageMixin, UpdateView):

    form_class = NewTaskForm
    object = None
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task was successfully modified')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, pk=self.kwargs['pk'])


class TaskDeleteView(LoginRequiredMixinWithMessage, SuccessMessageMixin, DeleteView):

    form_class = TaskDeleteForm
    template_name = 'tasks/del_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task was successfully deleted')

    """def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)"""
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task_author = Task.objects.get(id=task_id).author
        if request.user.id == task_author.id:
            return super().post(self, request, *args, **kwargs)
        messages.add_message(request, messages.ERROR, _("Only it's author can delete the task"))
        return redirect(reverse_lazy('tasks_index'))


class TaskInfoView(LoginRequiredMixinWithMessage, DetailView):

    model = Task
    template_name = 'tasks/task_info.html'
    login_url = reverse_lazy('login')
    context_object_name = 'task'

    """def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        labels = Label.objects.filter(task__name=task.name)
        return render(request, 'tasks/task_info.html', context={'task': task,
                                                                'labels': labels})"""
