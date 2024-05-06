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
        statuses = Status.objects.all().order_by('pk')
        return render(request, 'statuses/statuses.html', context={'statuses': statuses})


class NewStatusView(View):

    def get(self, request, *args, **kwargs):
        form = NewStatusForm()
        return render(request, 'statuses/new_status.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = NewStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Statussuccessfullycreated'))
            return redirect('statuses_list')


class StatusEditView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status = Status.objects.get(pk=self.kwargs['pk'])
            form = NewStatusForm(instance=status)
            return render(request, 'statuses/new_status.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = NewStatusForm(request.POST)
        if form.is_valid():
            Status.objects.filter(pk=self.kwargs['pk']).update(**form.cleaned_data)
            messages.success(request, _('Statuschangedsuccessfully'))
            return redirect('statuses_list')


class StatusDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            delete_form = StatusDeleteForm()
            status = Status.objects.get(pk=self.kwargs['pk'])
            return render(request, 'statuses/del_status.html',
                          context={'form': delete_form, 'status': status})

    def post(self, request, *args, **kwargs):
        status = Status.objects.get(pk=self.kwargs['pk'])
        status.delete()
        messages.success(request, _('Statusdeletedsuccessfully'))
        return redirect('statuses_list')
