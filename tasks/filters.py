import django_filters
from .models import Task
from labels.models import Label
from django import forms
from django.utils.translation import gettext as _


class TaskFilter(django_filters.FilterSet):

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        label_suffix='',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    self_tasks = django_filters.BooleanFilter(
        field_name='author',
        label=_('Only your tasks'),
        label_suffix='',
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            """taskautor = f'{self.request.user.first_name} {self.request.user.last_name}'
            return queryset.filter(taskautor=taskautor)"""
            author = self.request.user
            return queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
