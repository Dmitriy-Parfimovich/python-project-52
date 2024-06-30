from django.urls import path
from users.views import (UsersListView,
                         NewUserRegView,
                         UserEditView,
                         UserDeleteView)


# Create your views here.
urlpatterns = [
    path('', UsersListView.as_view(), name='users_list'),
    path('create/', NewUserRegView.as_view(), name='new_user_reg'),
    path('<int:pk>/update/', UserEditView.as_view(), name='user_edit'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
