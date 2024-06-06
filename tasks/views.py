#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from tasks.models import Task
from statuses.models import Status
from users.models import User
from labels.models import Label
from tasks.forms import NewTaskForm, TaskDeleteForm, FilterTaskForm
from django.utils.translation import gettext as _


# Create your views here.
class TasksListView(View):

    def get(self, request, *args, **kwargs):
        form = FilterTaskForm()
        tasks = Task.objects.all().order_by('pk')
        request_GET, self_tasks = False, False
        if request.GET:
            request_GET = True
            form = FilterTaskForm(request.GET)
            if 'self_tasks' in request.GET:
                tasks = tasks.filter(taskautor=request.user).order_by('pk')
                self_tasks = True
            if request.GET['status']:
                status = request.GET['status']
                tasks = tasks.filter(status=status).order_by('pk')
            if request.GET['executor']:
                taskexecutor = request.GET['executor']
                tasks = tasks.filter(executor=taskexecutor).order_by('pk')
        statuses = Status.objects.all().order_by('pk')
        taskexecutors = User.objects.all().order_by('pk')
        labels = Label.objects.all().order_by('pk')
        return render(request, 'tasks/tasks.html', context={'form': form,
                                                            'tasks': tasks,
                                                            'statuses': statuses,
                                                            'taskexecutors': taskexecutors,
                                                            'labels': labels,
                                                            'request_GET': request_GET,
                                                            'self_tasks': self_tasks,
                                                            })


class NewTaskView(View):

    def get(self, request, *args, **kwargs):
        form = NewTaskForm()
        statuses = Status.objects.all().order_by('pk')
        taskexecutors = User.objects.all().order_by('pk')
        labels = Label.objects.all().order_by('pk')
        return render(request, 'tasks/new_task.html', context={'form': form,
                                                               'statuses': statuses,
                                                               'taskexecutors': taskexecutors,
                                                               'labels': labels,
                                                               })

    def post(self, request, *args, **kwargs):
        form = NewTaskForm(request.POST)
        statuses = Status.objects.all().order_by('pk')
        taskexecutors = User.objects.all().order_by('pk')
        labels = Label.objects.all().order_by('pk')
        if form.is_valid():
            form.cleaned_data['taskautor'] = request.user
            form.save()
            messages.success(request, _('Task created successfully'))
            return redirect('tasks_list')
        return render(request, 'tasks/new_task.html', context={'form': form,
                                                               'statuses': statuses,
                                                               'taskexecutors': taskexecutors,
                                                               'labels': labels,
                                                               })


class TaskEditView(View):

    def get(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
        form = NewTaskForm(request.POST)
        statuses = Status.objects.all().order_by('pk')
        taskexecutors = User.objects.all().order_by('pk')
        labels = Label.objects.all().order_by('pk')
        edit_flag, task_error = True, False
        form.errors.clear()
        if form.is_valid():
            task = Task.objects.get(pk=self.kwargs['pk'])
            if Task.objects.filter(taskname=form['taskname'].value()).exists():
                task_to_edit_from_form = Task.objects.get(taskname=form['taskname'].value())
                if task.taskname != task_to_edit_from_form.taskname:
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
            task.taskname = form['taskname'].value()
            task.taskdescription = form.cleaned_data['taskdescription']
            task.executor = form.cleaned_data['executor']
            task.status = form.cleaned_data['status']
            task.save()
            labels = form.cleaned_data['labels']
            task.labels.set(labels)
            messages.success(request, _('The task was successfully modified'))
            return redirect('tasks_list')


class TaskDeleteView(View):

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        if task.taskautor == request.user.username:
            delete_form = TaskDeleteForm()
            return render(request, 'tasks/del_task.html',
                          context={'form': delete_form, 'task': task})
        else:
            messages.error(request, _("Only it's author can delete the task"))
            return redirect('tasks_list')

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        task.delete()
        messages.success(request, _('The task was successfully deleted'))
        return redirect('tasks_list')


class TaskInfoView(View):

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        labels = Label.objects.filter(task__taskname=task.taskname)
        return render(request, 'tasks/task_info.html', context={'task': task,
                                                                'labels': labels})
