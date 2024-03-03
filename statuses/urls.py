from django.urls import path
from statuses.views import (StatusesListView,
                            NewStatusView,
                            StatusEditView,
                            StatusDeleteView)

# Create your views here.
urlpatterns = [
    path('', StatusesListView.as_view(), name='statuses_list'),
    path('create/', NewStatusView.as_view(), name='new_status_create'),
    path('<int:pk>/update/', StatusEditView.as_view(), name='status_edit'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
]
