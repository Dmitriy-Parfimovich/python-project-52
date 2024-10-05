from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from labels.models import Label
from labels.forms import NewLabelForm, LabelDeleteForm
from django.utils.translation import gettext as _
from labels.utils import Mixins
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class LabelsListView(Mixins, ListView):

    queryset = Label.objects.all().order_by('pk')
    context_object_name = 'labels'
    template_name = 'labels/labels.html'

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)


class NewLabelView(SuccessMessageMixin, Mixins, CreateView):

    form_class = NewLabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class LabelEditView(SuccessMessageMixin, Mixins, UpdateView):

    form_class = NewLabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label changed successfully')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class LabelDeleteView(SuccessMessageMixin, Mixins, DeleteView):

    form_class = LabelDeleteForm
    template_name = 'labels/del_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label deleted successfully')

    def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        label = self.get_object()
        if list(label.task_set.all()) == []:
            label.delete()
        else:
            messages.error(self.request, _("Can't remove the label because it's in use"))
        return super().form_valid(form)
