from django.contrib.messages.storage.base import BaseStorage
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils import timezone

from .models import Inbox, Message, MessageArchive


STORE_LEVELS = (30, 40)  # TODO move it to settings


class StorageMixin(object):
    """
    TODO: docstring
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
        if self.user.is_authenticated():
            inbox_messages = Inbox.objects.filter(user=self.user).select_related("message")
        else:
            inbox_messages = []
        return messages + [im.message for im in inbox_messages], all_retrieved

    def add(self, level, message, extra_tags=''):
        """
        If the message level was configured for being stored and request.user
        is not anonymous, save it to the database. Otherwise, let some other
        class handle the message.

        Notice: controls like checking the message is not empty and the level
        is above the filter need to be performed here, but it could happen
        they'll be performed again later if the message does not need to be
        stored.
        """
        if not message:
            return
        # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return
        # Check if the message doesn't have a level that needs to be persisted
        if level not in STORE_LEVELS:
            return super(StorageMixin, self).add(level, message, extra_tags)

        self.added_new = True
        m = Message.objects.create(message=message, level=level, tags=extra_tags)
        MessageArchive.objects.create(user=self.user, message=m)
        self._queued_messages.append(m)

    def _store(self, messages, response, *args, **kwargs):
        """
        persistent messages are already in the database, so we can say they're already "stored"
        Here we put them in the inbox, or remove from the inbox in case the messages were
        iterated.

        messages contains only new msgs if self.used==True
        else contains both new and unread messages
        """
        contrib_messages = []
        if self.user.is_authenticated():
            if not messages:
                # erase inbox
                Inbox.objects.filter(user=self.user).delete()
            else:
                for m in messages:
                    if isinstance(m, Message):
                        # create inbox for the message if does not already exists
                        Inbox.objects.get_or_create(user=self.user, message=m)
                    else:
                        contrib_messages.append(m)

        super(StorageMixin, self)._store(contrib_messages, response, *args, **kwargs)

    def _prepare_messages(self, messages):
        """
        Prepares a list of messages for storage.
        """
        for message in messages:
            if not isinstance(message, Message):
                message._prepare()


class PersistentStorage(StorageMixin, FallbackStorage):
    """
    TODO: docstring
    """
    pass
