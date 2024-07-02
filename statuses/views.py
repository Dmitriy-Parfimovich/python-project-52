#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from statuses.models import Status
from statuses.forms import NewStatusForm, StatusDeleteForm
from django.utils.translation import gettext as _


# Create your views here.
class StatusesListView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            statuses = Status.objects.all().order_by('pk')
            return render(request, 'statuses/statuses.html', context={'statuses': statuses})
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')


class NewStatusView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = NewStatusForm()
            return render(request, 'statuses/new_status.html', context={'form': form})
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        form = NewStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully created'))
            return redirect('statuses_list')
        return render(request, 'statuses/new_status.html', context={'form': form})


class StatusEditView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status = Status.objects.get(pk=self.kwargs['pk'])
            form = NewStatusForm(instance=status)
            return render(request, 'statuses/new_status.html', context={'form': form})
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        form = NewStatusForm(request.POST)
        if form.is_valid():
            Status.objects.filter(pk=self.kwargs['pk']).update(**form.cleaned_data)
            messages.success(request, _('Status changed successfully'))
            return redirect('statuses_list')


class StatusDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status = Status.objects.get(pk=self.kwargs['pk'])
            delete_form = StatusDeleteForm()
            return render(request, 'statuses/del_status.html',
                          context={'form': delete_form, 'status': status})
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        status = Status.objects.get(pk=self.kwargs['pk'])
        if list(status.task_set.all()) == []:
            status.delete()
            messages.success(request, _('Status deleted successfully'))
            return redirect('statuses_list')
        else:
            messages.error(request, _("Can't delete a status because it's in use"))
            return redirect('statuses_list')
