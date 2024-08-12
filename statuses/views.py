from typing import Any
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from statuses.models import Status
from statuses.forms import NewStatusForm, StatusDeleteForm
from django.utils.translation import gettext as _


# Create your views here.
class StatusesListView(ListView):

    queryset = Status.objects.all().order_by('pk')
    context_object_name = 'statuses'
    template_name = 'statuses/statuses.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')


class NewStatusView(CreateView):

    form_class = NewStatusForm
    template_name = 'statuses/new_status.html'
    success_url = reverse_lazy('statuses_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
    
    def form_valid(self, form):
        messages.success(self.request, _('Status successfully created'))
        return super().form_valid(form)


class StatusEditView(UpdateView):

    model = Status
    form_class = NewStatusForm
    template_name = 'statuses/new_status.html'
    success_url = reverse_lazy('statuses_list')

    def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
    
    def form_valid(self, form):
        status = self.get_object()
        status.name = form.cleaned_data['name']
        status.save()
        messages.success(self.request, _('Status changed successfully'))
        return super().form_valid(form)


class StatusDeleteView(DeleteView):

    model = Status
    form_class = StatusDeleteForm
    template_name = 'statuses/del_status.html'
    success_url = reverse_lazy('statuses_list')

    def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')
    
    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if list(status.task_set.all()) == []:
            status.delete()
            messages.success(request, _('Status deleted successfully'))
        else:
            messages.error(request, _("Can't delete a status because it's in use"))
        return redirect('statuses_list')
