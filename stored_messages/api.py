from .settings import stored_messages_settings


__all__ = (
    'add_message_for',
    'broadcast_message',
    'mark_read',
    'mark_all_read',
)


def add_message_for(users, level, message_text, extra_tags='', date=None, url=None, fail_silently=False):
    """
    Send a message to a list of users without passing through `django.contrib.messages`

    :param users: an iterable containing the recipients of the messages
    :param level: message level
    :param message_text: the string containing the message
    :param extra_tags: like the Django api, a string containing extra tags for the message
    :param date: a date, different than the default timezone.now
    :param url: an optional url
    :param fail_silently: not used at the moment
    """
    BackendClass = stored_messages_settings.STORAGE_BACKEND
    backend = BackendClass()
    m = backend.create_message(level, message_text, extra_tags, date, url)
    backend.archive_store(users, m)
    backend.inbox_store(users, m)


def broadcast_message(level, message_text, extra_tags='', date=None, url=None, fail_silently=False):
    """
    Send a message to all users aka broadcast.

    :param level: message level
    :param message_text: the string containing the message
    :param extra_tags: like the Django api, a string containing extra tags for the message
    :param date: a date, different than the default timezone.now
    :param url: an optional url
    :param fail_silently: not used at the moment
    """
    from django.contrib.auth import get_user_model
    users = get_user_model().objects.all()
    add_message_for(users, level, message_text, extra_tags=extra_tags, date=date, url=url, fail_silently=fail_silently)


def mark_read(user, message):
    """
    Mark message instance as read for user.
    Returns True if the message was `unread` and thus actually marked as `read` or False in case
    it is already `read` or it does not exist at all.

    :param user: user instance for the recipient
    :param message: a Message instance to mark as read
    """
    BackendClass = stored_messages_settings.STORAGE_BACKEND
    backend = BackendClass()
    backend.inbox_delete(user, message)


def mark_all_read(user):
    """
    Mark all message instances for a user as read.

    :param user: user instance for the recipient
    """
    BackendClass = stored_messages_settings.STORAGE_BACKEND
    backend = BackendClass()
    backend.inbox_purge(user)
