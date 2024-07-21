from typing import Any
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from statuses.models import Status
from statuses.forms import NewStatusForm, StatusDeleteForm
from django.utils.translation import gettext as _


# Create your views here.
#class StatusesListView(View):

#    def get(self, request, *args, **kwargs):
#        if request.user.is_authenticated:
#            statuses = Status.objects.all().order_by('pk')
#            return render(request, 'statuses/statuses.html', context={'statuses': statuses})
#        messages.error(request, _('You are not authorized! Please log in.'))
#        return redirect('login')

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

    
"""class NewStatusView(View):

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
"""

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


"""class StatusEditView(View):

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
"""

class StatusEditView(UpdateView):

    model = Status
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
        messages.success(self.request, _('Status changed successfully'))
        return super().form_valid(form)


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
