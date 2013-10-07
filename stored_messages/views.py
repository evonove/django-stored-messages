from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Inbox
from .serializers import InboxSerializer


class InboxViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides `list` and `detail` actions, plus a `read` POST endpoint for
    marking inbox messages as read.
    """
    serializer_class = InboxSerializer
    model = Inbox

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Inbox.objects.filter(user=self.request.user)
        return Inbox.objects.none()

    @action()
    def read(self, request, pk=None):
        """
        Mark the message as read (i.e. delete from inbox)
        """
        inbox_m = self.get_object()
        inbox_m.delete()
        return Response({'status': 'message marked as read'})
