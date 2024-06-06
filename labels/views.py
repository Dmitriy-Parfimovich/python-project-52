#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from labels.models import Label
from labels.forms import NewLabelForm, LabelDeleteForm
from django.utils.translation import gettext as _


# Create your views here.
class LabelsListView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all().order_by('pk')
        return render(request, 'labels/labels.html', context={'labels': labels})


class NewLabelView(View):

    def get(self, request, *args, **kwargs):
        form = NewLabelForm()
        return render(request, 'labels/new_label.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = NewLabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully created'))
            return redirect('labels_list')


class LabelEditView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            label = Label.objects.get(pk=self.kwargs['pk'])
            form = NewLabelForm(instance=label)
            return render(request, 'labels/new_label.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = NewLabelForm(request.POST)
        if form.is_valid():
            Label.objects.filter(pk=self.kwargs['pk']).update(**form.cleaned_data)
            messages.success(request, _('Label changed successfully'))
            return redirect('labels_list')


class LabelDeleteView(View):

    def get(self, request, *args, **kwargs):
        label = Label.objects.get(pk=self.kwargs['pk'])
        if list(label.task_set.all()) == []:
            delete_form = LabelDeleteForm()
            return render(request, 'labels/del_label.html',
                          context={'form': delete_form, 'label': label})
        else:
            messages.error(request, _("Can't remove the label because it's in use"))
            return redirect('labels_list')

    def post(self, request, *args, **kwargs):
        label = Label.objects.get(pk=self.kwargs['pk'])
        label.delete()
        messages.success(request, _('Label deleted successfully'))
        return redirect('labels_list')
