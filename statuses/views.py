from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)
from statuses.models import Status
from statuses.forms import NewStatusForm
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.permissions import LoginRequiredMixinWithMessage


# Create your views here.
class StatusesListView(LoginRequiredMixinWithMessage, ListView):

    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/statuses.html'


class NewStatusView(LoginRequiredMixinWithMessage, SuccessMessageMixin, CreateView):

    form_class = NewStatusForm
    template_name = 'statuses/new_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully created')


class StatusEditView(LoginRequiredMixinWithMessage, SuccessMessageMixin, UpdateView):

    model = Status
    form_class = NewStatusForm
    template_name = 'statuses/new_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status changed successfully')


class StatusDeleteView(LoginRequiredMixinWithMessage, SuccessMessageMixin, DeleteView):

    model = Status
    template_name = 'statuses/del_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status deleted successfully')

    def form_valid(self, form):
        status = self.get_object()
        if list(status.task_set.all()) != []:
            messages.error(self.request, _("Can't delete a status because it's in use"))
        return super().form_valid(form)
