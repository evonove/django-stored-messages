from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from .serializers import InboxSerializer
from .settings import stored_messages_settings


class InboxViewSet(viewsets.ViewSet):
    """
    Provides `list` and `detail` actions, plus a `read` POST endpoint for
    marking inbox messages as read.
    """
    def list(self, request):
        backend = stored_messages_settings.STORAGE_BACKEND()
        messages = backend.inbox_list(request.user)
        serializer = InboxSerializer(messages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pass

    @action()
    def read(self, request, pk=None):
        """
        Mark the message as read (i.e. delete from inbox)
        """
        inbox_m = self.get_object()
        inbox_m.delete()
        return Response({'status': 'message marked as read'})


@login_required
@api_view(['POST'])
def mark_all_read(request):
    """
    Mark all messages as read (i.e. delete from inbox) for current logged in user
    """
    backend = stored_messages_settings.STORAGE_BACKEND()
    backend.inbox_purge(request.user)
    return Response({"message": "All messages read"})
