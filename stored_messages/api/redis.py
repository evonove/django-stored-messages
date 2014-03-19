import redis

STORED_MESSAGES_REDIS = getattr(settings, 'STORED_MESSAGES_REDIS', {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
})

def _redis_client():
        return redis.StrictRedis(host=STORED_MESSAGES_REDIS.get('host'),
                                 port=STORED_MESSAGES_REDIS.get('port'),
                                 db=STORED_MESSAGES_REDIS.get('db'))

def add_message_for(users, level, message, extra_tags='', fail_silently=False):
    """
    Send a message to a list of users without passing through `django.contrib.messages`

    :param users: an iterable containing the recipients of the messages
    :param level: message level
    :param message: the string containing the message
    :param extra_tags: like the Django api, a string containing extra tags for the message
    :param fail_silently: not used at the moment
    """
    c = _redis_client()
    m = {'message': message, 'level': level, 'tags': extra_tags)
    for u in users:
        c.sadd('user:%d:notifications' % user.pk, m)


def broadcast_message(level, message, extra_tags='', fail_silently=False):
    """
    Send a message to all users in the system. TODO.
    """
    # TODO
    raise NotImplementedError


def mark_read(user, message):
    """
    Mark message instance as read for user.
    Returns True if the message was `unread` and thus actually marked as `read` or False in case
    it is already `read` or it does not exist at all.

    :param user: user instance for the recipient
    :param message: a Message instance to mark as read
    """
    c = _redis_client()
    return c.srem('user:%d:notifications' % user.pk, message)


def mark_all_read(user):
    """
    Mark all message instances for a user as read.

    :param user: user instance for the recipient
    """
    c = _redis_client()
    c.delete('user:%d:notifications' % user.pk, m)
