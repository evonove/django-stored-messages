from django.contrib.messages.storage.base import BaseStorage
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils import timezone

from .models import Inbox, Message, MessageArchive


STORE_LEVELS = (30, 40)  # TODO move it to settings


class StorageMixin(object):
    """

    """
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        super(StorageMixin, self).__init__(request, *args, **kwargs)

    def _get(self, *args, **kwargs):
        """
        Retrieve unread messages for current user, both from the inbox and
        from other storages
        """
        messages, all_retrieved = super(StorageMixin, self)._get(*args, **kwargs)
        inbox_messages = Inbox.objects.filter(user=self.user).select_related("message")
        return messages + [im.message for im in inbox_messages], all_retrieved

    def add(self, level, message, extra_tags=''):
        """
        If the message level was configured for being stored save it to the database.
        Otherwise, let some other class handle the message.

        Notice: controls like checking the message is not empty and the level is above the filter
        need to be performed here, but it could happen they'll be performed again later if the
        message does not need to be stored.
        """
        if not message:
            return
        # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return
        # Check if the message has to be persisted
        if level in STORE_LEVELS:
            m = Message.objects.get_or_create(message=message, level=level, tags=extra_tags)[0]
            MessageArchive.objects.create(user=self.user, message=m, date=timezone.now())
            Inbox.objects.create(user=self.user, message=m)
        else:
            super(StorageMixin, self).add(level, message, extra_tags)


class PersistentStorage(StorageMixin, FallbackStorage):
    pass
