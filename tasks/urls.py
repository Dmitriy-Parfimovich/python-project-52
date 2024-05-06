from django.urls import path
from tasks.views import (TasksListView,
                         NewTaskView,
                         TaskEditView,
                         TaskDeleteView,
                         TaskInfoView)

# Create your views here.
urlpatterns = [
    path('', TasksListView.as_view(), name='tasks_list'),
    path('create/', NewTaskView.as_view(), name='new_task_create'),
    path('<int:pk>/', TaskInfoView.as_view(), name='task_info'),
    path('<int:pk>/update/', TaskEditView.as_view(), name='task_edit'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
