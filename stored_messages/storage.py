from django.contrib.messages.storage.base import BaseStorage
from django.utils import timezone

from .models import Inbox, Message, MessageArchive


class Storage(BaseStorage):
    """

    """
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        super(Storage, self).__init__(request, *args, **kwargs)

    def _get(self, *args, **kwargs):
        """
        Retrieve unread messages for current user
        """
        inbox_messages = Inbox.objects.filter(user=self.user).select_related("message")
        return [im.message for im in inbox_messages], True

    def _store(self, messages, response, *args, **kwargs):
        for message in messages:
            m = Message.objects.create(message=message.message, level=message.level,
                                       tags=message.tags, date=timezone.now())
            MessageArchive.objects.create(user=self.user, message=m)
            Inbox.objects.create(user=self.user, message=m)
