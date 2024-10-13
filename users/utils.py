from users.models import User
from django.views.generic.detail import SingleObjectMixin


class Mixins(SingleObjectMixin):

    model = User

    def get_mixin_context(self, context, **kwargs):
        if kwargs['pk'] and self.request.user == self.get_object():
            context['user'] = self.get_object()
        return context
