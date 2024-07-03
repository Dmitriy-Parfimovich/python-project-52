import django_filters
from .models import Task
from django_filters import CharFilter


class TaskFilter(django_filters.FilterSet):
    status = CharFilter(field_name='status', lookup_expr='exact')
    executor = CharFilter(field_name='executor', lookup_expr='exact')
    labels = CharFilter(field_name='labels', lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
