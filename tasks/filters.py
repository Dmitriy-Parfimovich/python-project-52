import django_filters
from .models import Task
from labels.models import Label
from django import forms
from django_filters import CharFilter
from django.utils.translation import gettext as _


"""class TaskFilter(django_filters.FilterSet):
    status = CharFilter(field_name='status', lookup_expr='exact')
    executor = CharFilter(field_name='executor', lookup_expr='exact')
    labels = CharFilter(field_name='labels', lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']"""

class TaskFilter(django_filters.FilterSet):

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        label_suffix='',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    self_tasks = django_filters.BooleanFilter(
        field_name='taskautor',
        label=_('Only your tasks'),
        label_suffix='',
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            # user_id = self.request.user.id
            taskautor = f'{self.request.user.first_name} {self.request.user.last_name}'
            return queryset.filter(taskautor=taskautor)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']


    """class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']"""
