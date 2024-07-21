from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView
from tasks.models import Task
from statuses.models import Status
from users.models import User
from labels.models import Label
from tasks.forms import NewTaskForm, TaskDeleteForm
from django.utils.translation import gettext as _
from .filters import TaskFilter


# Create your views here.
#class TasksListView(View):

#    def get(self, request, *args, **kwargs):
#        if request.user.is_authenticated:
#            tasks = Task.objects.all()
#            request_GET, self_tasks = False, False
#            if request.GET:
#                request_GET = True
#                if 'self_tasks' in request.GET:
#                    taskautor = f'{request.user.first_name} {request.user.last_name}'
#                    tasks = tasks.filter(taskautor=taskautor)
#                    self_tasks = True
#            myFilter = TaskFilter(request.GET, queryset=tasks)
#            tasks = myFilter.qs.order_by('pk')
#            statuses = Status.objects.all().order_by('pk')
#            taskexecutors = User.objects.all().order_by('pk')
#            labels = Label.objects.all().order_by('pk')
#            context = {
#                'form': myFilter.form,
#                'tasks': tasks,
#                'statuses': statuses,
#                'taskexecutors': taskexecutors,
#                'labels': labels,
#                'request_GET': request_GET,
#                'self_tasks': self_tasks,
#            }
#            return render(request, 'tasks/tasks.html', context)
#        messages.error(request, _('You are not authorized! Please log in.'))
#        return redirect('login')


class TasksListView(ListView):

    queryset = Task.objects.all()
    object_list = None
    template_name = 'tasks/tasks.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['statuses'] = Status.objects.all().order_by('pk')  
        context['taskexecutors'] = User.objects.all().order_by('pk')  
        context['labels'] = Label.objects.all().order_by('pk')
        context['request_GET'] = False
        context['self_tasks'] = False
        return context
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
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
        return render(request, self.template_name, context)


"""class NewTaskView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = NewTaskForm()
            statuses = Status.objects.all().order_by('pk')
            taskexecutors = User.objects.all().order_by('pk')
            labels = Label.objects.all().order_by('pk')
            return render(request, 'tasks/new_task.html', context={'form': form,
                                                                   'statuses': statuses,
                                                                   'taskexecutors': taskexecutors,
                                                                   'labels': labels,
                                                                   })
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        form = NewTaskForm(request.POST)
        statuses = Status.objects.all().order_by('pk')
        taskexecutors = User.objects.all().order_by('pk')
        labels = Label.objects.all().order_by('pk')
        if form.is_valid():
            taskautor = f'{request.user.first_name} {request.user.last_name}'
            form.cleaned_data['taskautor'] = taskautor
            form.save()
            messages.success(request, _('Task created successfully'))
            return redirect('tasks_list')
        return render(request, 'tasks/new_task.html', context={'form': form,
                                                               'statuses': statuses,
                                                               'taskexecutors': taskexecutors,
                                                               'labels': labels,
                                                               })
"""


class NewTaskView(CreateView):

    form_class = NewTaskForm
    template_name = 'tasks/new_task.html'
    success_url = reverse_lazy('tasks_list')

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['statuses'] = Status.objects.all().order_by('pk')  
        context['taskexecutors'] = User.objects.all().order_by('pk')  
        context['labels'] = Label.objects.all().order_by('pk')
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
    
    def form_valid(self, form):
        taskautor = f'{self.request.user.first_name} {self.request.user.last_name}'
        form.cleaned_data['taskautor'] = taskautor
        messages.success(self.request, _('Task created successfully'))
        return super().form_valid(form)


class TaskEditView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            edit_flag = True
            task = Task.objects.get(pk=self.kwargs['pk'])
            form = NewTaskForm(instance=task)
            statuses = Status.objects.all().order_by('pk')
            taskexecutors = User.objects.all().order_by('pk')
            labels = Label.objects.all().order_by('pk')
            return render(request, 'tasks/new_task.html', context={'form': form,
                                                                   'statuses': statuses,
                                                                   'taskexecutors': taskexecutors,
                                                                   'labels': labels,
                                                                   'edit_flag': edit_flag,
                                                                   })
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        form = NewTaskForm(request.POST)
        statuses = Status.objects.all().order_by('pk')
        taskexecutors = User.objects.all().order_by('pk')
        labels = Label.objects.all().order_by('pk')
        edit_flag, task_error = True, False
        form.errors.clear()
        if form.is_valid():
            task = Task.objects.get(pk=self.kwargs['pk'])
            if Task.objects.filter(name=form['name'].value()).exists():
                task_to_edit_from_form = Task.objects.get(name=form['name'].value())
                if task.name != task_to_edit_from_form.name:
                    task_error = True
                    return render(request,
                                  'tasks/new_task.html',
                                  context={'form': form,
                                           'statuses': statuses,
                                           'taskexecutors': taskexecutors,
                                           'labels': labels,
                                           'edit_flag': edit_flag,
                                           'task_error': task_error,
                                           })
            task.name = form['name'].value()
            task.description = form.cleaned_data['description']
            task.executor = form.cleaned_data['executor']
            task.status = form.cleaned_data['status']
            task.save()
            labels = form.cleaned_data['labels']
            task.labels.set(labels)
            messages.success(request, _('The task was successfully modified'))
            return redirect('tasks_list')


class TaskDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            task = Task.objects.get(pk=self.kwargs['pk'])
            if task.taskautor == f'{request.user.first_name} {request.user.last_name}':
                delete_form = TaskDeleteForm()
                return render(request, 'tasks/del_task.html',
                              context={'form': delete_form, 'task': task})
            else:
                messages.error(request, _("Only it's author can delete the task"))
                return redirect('tasks_list')
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        task.delete()
        messages.success(request, _('The task was successfully deleted'))
        return redirect('tasks_list')


class TaskInfoView(View):

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        labels = Label.objects.filter(task__name=task.name)
        return render(request, 'tasks/task_info.html', context={'task': task,
                                                                'labels': labels})
