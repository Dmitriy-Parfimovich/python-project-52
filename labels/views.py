from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from labels.models import Label
from labels.forms import NewLabelForm
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.permissions import LoginRequiredMixinWithMessage


# Create your views here.
class LabelsListView(LoginRequiredMixinWithMessage, ListView):

    queryset = Label.objects.all().order_by('pk')
    context_object_name = 'labels'
    template_name = 'labels/labels.html'


class NewLabelView(LoginRequiredMixinWithMessage, SuccessMessageMixin, CreateView):

    form_class = NewLabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')


class LabelEditView(LoginRequiredMixinWithMessage, SuccessMessageMixin, UpdateView):

    model = Label
    form_class = NewLabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label changed successfully')


class LabelDeleteView(LoginRequiredMixinWithMessage, SuccessMessageMixin, DeleteView):

    model = Label
    template_name = 'labels/del_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label deleted successfully')

    def form_valid(self, form):
        label = self.get_object()
        if list(label.task_set.all()) != []:
            messages.error(self.request, _("Can't remove the label because it's in use"))
        return super().form_valid(form)
