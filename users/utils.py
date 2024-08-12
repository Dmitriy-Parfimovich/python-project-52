from users.models import User
from django.views.generic.detail import SingleObjectMixin

class UserDataMixin(SingleObjectMixin):

    model = User

    """def get_object(self):
        queryset = User.objects.all()
        return queryset.get(pk=self.kwargs['pk'])"""
    
    def get_mixin_context(self, context, **kwargs):
        kwargs['user_is_auth'] = False
        if self.request.user.is_authenticated:
            kwargs['user_is_auth'] = True
        if kwargs['pk']:
            if self.request.user == self.get_object():
                kwargs['user'] = self.get_object()
        context.update(kwargs)
        return context
