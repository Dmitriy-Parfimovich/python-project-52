from users.models import User
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
