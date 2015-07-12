from django.utils import timezone

from ..base import StoredMessagesBackend
from ..exceptions import MessageTypeNotSupported, MessageDoesNotExist
from .. import signals
from ...models import Inbox, Message, MessageArchive
from ...settings import stored_messages_settings


class DefaultBackend(StoredMessagesBackend):
    """

    """
    def inbox_list(self, user):
        if user.is_anonymous():
            return []
        inbox = Inbox.objects.filter(user=user).select_related("message")
        return [m.message for m in inbox]

    def inbox_purge(self, user):
        if user.is_authenticated():
            Inbox.objects.filter(user=user).delete()
            signals.inbox_purged.send(sender=self.__class__, user=user)

    def inbox_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            Inbox.objects.get_or_create(user=user, message=msg_instance)
            signals.inbox_stored.send(sender=self.__class__, user=user, message=msg_instance)

    def inbox_delete(self, user, msg_id):
        try:
            inbox_m = Inbox.objects.filter(user=user, message=msg_id).get()
            inbox_m.delete()
            signals.inbox_deleted.send(sender=self.__class__, user=user, message_id=msg_id)
        except Inbox.DoesNotExist:
            raise MessageDoesNotExist("Message with id %s does not exist" % msg_id)

    def inbox_get(self, user, msg_id):
        try:
            return Inbox.objects.get(pk=msg_id).message
        except Inbox.DoesNotExist:
            raise MessageDoesNotExist("Message with id %s does not exist" % msg_id)

    def create_message(self, level, msg_text, extra_tags='', date=None, url=None):
        kwargs = {
            'message': msg_text,
            'level': level,
            'tags': extra_tags,
            'url': url,
        }
        if date:
            kwargs['date'] = date
        m_instance = Message.objects.create(**kwargs)
        return m_instance

    def archive_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            MessageArchive.objects.create(user=user, message=msg_instance)
            signals.archive_stored.send(sender=self.__class__, user=user, message=msg_instance)

    def archive_list(self, user):
        return list(MessageArchive.objects.filter(user=user))

    def can_handle(self, message):
        return isinstance(message, Message)

    def expired_messages_cleanup(self):
        expiration_date = timezone.now() + timezone.timedelta(
            days=-stored_messages_settings.MESSAGE_EXPIRE_DAYS)
        Message.objects.filter(date__lte=expiration_date).delete()

    def _flush(self):
        Inbox.objects.all().delete()
        MessageArchive.objects.all().delete()
        Message.objects.all().delete()
