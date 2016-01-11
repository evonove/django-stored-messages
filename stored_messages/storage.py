from django.contrib.messages.storage.fallback import FallbackStorage

from .settings import stored_messages_settings
from .backends.exceptions import MessageTypeNotSupported


class StorageMixin(object):
    """
    This mixin implements a message storage compliant with
    `django.contrib.messages` which stores messages on the database when
    needed, delegating to the sibling class otherwise. Messages are stored
    only when the user is authenticated and the message level is configured
    for being persisted. The mixin can be derived together with another class
    implementing a storage, tipically one of the three provided by Django out
    of the box.
    """
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        BackendClass = stored_messages_settings.STORAGE_BACKEND
        self.backend = BackendClass()
        super(StorageMixin, self).__init__(request, *args, **kwargs)

    def _get(self, *args, **kwargs):
        """
        Retrieve unread messages for current user, both from the inbox and
        from other storages
        """
        messages, all_retrieved = super(StorageMixin, self)._get(*args, **kwargs)
        if self.user.is_authenticated():
            inbox_messages = self.backend.inbox_list(self.user)
        else:
            inbox_messages = []

        return messages + inbox_messages, all_retrieved

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
        if level not in stored_messages_settings.STORE_LEVELS or self.user.is_anonymous():
            return super(StorageMixin, self).add(level, message, extra_tags)

        self.added_new = True
        m = self.backend.create_message(level, message, extra_tags)
        self.backend.archive_store([self.user], m)
        self._queued_messages.append(m)

    def _store(self, messages, response, *args, **kwargs):
        """
        persistent messages are already in the database inside the 'archive',
        so we can say they're already "stored".
        Here we put them in the inbox, or remove from the inbox in case the
        messages were iterated.

        messages contains only new msgs if self.used==True
        else contains both new and unread messages
        """
        contrib_messages = []
        if self.user.is_authenticated():
            if not messages:
                # erase inbox
                self.backend.inbox_purge(self.user)
            else:
                for m in messages:
                    try:
                        self.backend.inbox_store([self.user], m)
                    except MessageTypeNotSupported:
                        contrib_messages.append(m)

        super(StorageMixin, self)._store(contrib_messages, response, *args, **kwargs)

    def _prepare_messages(self, messages):
        """
        Like the base class method, prepares a list of messages for storage
        but avoid to do this for `models.Message` instances.
        """
        for message in messages:
            if not self.backend.can_handle(message):
                message._prepare()


class PersistentStorage(StorageMixin, FallbackStorage):
    """
    This class is provided for convenience: it implements `StorageMixin` which
    persists messages having a type configured to be persisted and passes
    other messages to `FallbackStorage`, one of the defaults provided by
    Django which stores messages inside cookies or sessions.
    """
    pass
