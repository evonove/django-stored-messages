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

    def create_message(self, user, level, msg_text, extra_tags):
        m_instance = Message.objects.create(message=msg_text, level=level, tags=extra_tags)
        MessageArchive.objects.create(user=user, message=m_instance)
        return m_instance

    def add_message_for(self, users, level, message, extra_tags='', fail_silently=False):
        pass

    def archive_list(self, user):
        return list(MessageArchive.objects.filter(user=user))

    def can_handle(self, message):
        return isinstance(message, Message)
