from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from labels.models import Label
from labels.forms import NewLabelForm, LabelDeleteForm
from django.utils.translation import gettext as _


# Create your views here.
class LabelsListView(ListView):

    queryset = Label.objects.all().order_by('pk')
    context_object_name = 'labels'
    template_name = 'labels/labels.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')


class NewLabelView(CreateView):

    form_class = NewLabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
    
    def form_valid(self, form):
        messages.success(self.request, _('Label successfully created'))
        return super().form_valid(form)


class LabelEditView(UpdateView):

    model = Label
    form_class = NewLabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
    
    def form_valid(self, form):
        messages.success(self.request, _('Label changed successfully'))
        return super().form_valid(form)


class LabelDeleteView(DeleteView):

    model = Label
    form_class = LabelDeleteForm
    template_name = 'labels/del_label.html'
    success_url = reverse_lazy('labels_list')

    def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You are not authorized! Please log in.'))
        return redirect('login')
    
    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if list(label.task_set.all()) == []:
            label.delete()
            messages.success(request, _('Label deleted successfully'))
        else:
            messages.error(request, _("Can't remove the label because it's in use"))
        return redirect('labels_list')
