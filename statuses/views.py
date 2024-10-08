from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from statuses.models import Status
from statuses.forms import NewStatusForm, StatusDeleteForm
from django.utils.translation import gettext as _
from statuses.utils import Mixins
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class StatusesListView(Mixins, ListView):

    queryset = Status.objects.all().order_by('pk')
    context_object_name = 'statuses'
    template_name = 'statuses/statuses.html'

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)


class NewStatusView(SuccessMessageMixin, Mixins, CreateView):

    form_class = NewStatusForm
    template_name = 'statuses/new_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully created')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class StatusEditView(SuccessMessageMixin, Mixins, UpdateView):

    form_class = NewStatusForm
    template_name = 'statuses/new_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status changed successfully')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        status = self.get_object()
        status.name = form.cleaned_data['name']
        status.save()
        return super().form_valid(form)


class StatusDeleteView(SuccessMessageMixin, Mixins, DeleteView):

    form_class = StatusDeleteForm
    template_name = 'statuses/del_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status deleted successfully')

    def dispatch(self, request, *args, **kwargs):
        return self.mixin_dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        status = self.get_object()
        if list(status.task_set.all()) == []:
            status.delete()
        else:
            messages.error(self.request, _("Can't delete a status because it's in use"))
        return super().form_valid(form)
