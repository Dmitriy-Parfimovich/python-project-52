from django.urls import path
from labels.views import (LabelsListView,
                          NewLabelView,
                          LabelEditView,
                          LabelDeleteView)

# Create your views here.
urlpatterns = [
    path('', LabelsListView.as_view(), name='labels_list'),
    path('create/', NewLabelView.as_view(), name='new_label_create'),
    path('<int:pk>/update/', LabelEditView.as_view(), name='label_edit'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='label_delete'),
]
