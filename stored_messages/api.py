from .models import Inbox

__all__ = (
    'add_message_for', 'broadcast_message',
    'mark_read',
)


def add_message_for(users, level, message, extra_tags='', fail_silently=False):
    """
    Send a message to a list of users
    """
    pass


def broadcast_message(level, message, extra_tags='', fail_silently=False):
    """
    Send a message to all users in the system
    """
    pass


def mark_read(user, message):
    """
    Mark message as read for user.
    """
    Inbox.objects.filter(user=user, message=message).delete()
