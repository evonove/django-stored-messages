from ..base import StoredMessagesBackend
from ...models import Inbox, Message, MessageArchive


class DefaultBackend(StoredMessagesBackend):
    """

    """
    def inbox_list(self, user):
        return list(Inbox.objects.filter(user=user).select_related("message"))

    def inbox_purge(self, user):
        Inbox.objects.filter(user=user).delete()

    def inbox_get_or_create(self, user, message):
        if isinstance(message, Message):
            Inbox.objects.get_or_create(user=user, message=message)

    def create_message(self, user, message, level, extra_tags):
        m_instance = Message.objects.create(message=message, level=level, tags=extra_tags)
        MessageArchive.objects.create(user=user, message=m_instance)
        return m_instance

    def archive_list(self, user):
        return list(MessageArchive.objects.filter(user=user))

    def can_handle(self, message):
        return isinstance(message, Message)
