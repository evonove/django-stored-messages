from ..base import StoredMessagesBackend
from ..exceptions import MessageTypeNotSupported, InboxDoesNotExist
from ...models import Inbox, Message, MessageArchive


class DefaultBackend(StoredMessagesBackend):
    """

    """
    def inbox_list(self, user):
        return list(Inbox.objects.filter(user=user).select_related("message"))

    def inbox_purge(self, user):
        Inbox.objects.filter(user=user).delete()

    def inbox_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            Inbox.objects.get_or_create(user=user, message=msg_instance)

    def inbox_delete(self, user, msg_instance):
        try:
            inbox_m = Inbox.objects.filter(user=user, message=msg_instance).get()
            inbox_m.delete()
        except Inbox.DoesNotExist:
            raise InboxDoesNotExist()

    def create_message(self, level, msg_text, extra_tags):
        m_instance = Message.objects.create(message=msg_text, level=level, tags=extra_tags)
        return m_instance

    def archive_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            MessageArchive.objects.create(user=user, message=msg_instance)

    def archive_list(self, user):
        return list(MessageArchive.objects.filter(user=user))

    def can_handle(self, message):
        return isinstance(message, Message)
