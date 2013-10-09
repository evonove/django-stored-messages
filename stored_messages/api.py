
__all__ = (
    'add_message_for', 'broadcast_message',
    'mark_read',
)

from .models import Message, MessageArchive, Inbox


def add_message_for(users, level, message, extra_tags='', fail_silently=False):
    """
    Send a message to a list of users without passing through `django.contrib.messages`
    """
    m = Message.objects.create(message=message, level=level, tags=extra_tags)
    for u in users:
        MessageArchive.objects.create(user=u, message=m)
        Inbox.objects.create(user=u, message=m)


def broadcast_message(level, message, extra_tags='', fail_silently=False):
    """
    Send a message to all users in the system
    """
    # TODO
    raise NotImplementedError


def mark_read(user, message):
    """
    Mark message as read for user.

    :return: Whatever the message was actually deleted
    """
    from .models import Inbox
    try:
        inbox_m = Inbox.objects.filter(user=user, message=message).get()
        inbox_m.delete()
        return True
    except Inbox.DoesNotExist:
        return False
