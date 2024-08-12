from users.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin

class UserDataMixin(SingleObjectMixin):

    model = User

    """def get_object(self):
        queryset = User.objects.all()
        return queryset.get(pk=self.kwargs['pk'])"""
    
    def get_mixin_context(self, context, **kwargs):
        context['user_is_auth'] = False
        if kwargs['pk'] and self.request.user == self.get_object():
                context['user'] = self.get_object()
        elif self.request.user.is_authenticated:
            context['user_is_auth'] = True
        return context
    
    def mixin_dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.request.user != self.get_object():
                messages.error(request, _('You do not have permission to change\
                                          another user.'))
                return redirect('users_list')
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
