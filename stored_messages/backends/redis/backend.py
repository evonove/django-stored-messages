import redis

from ..base import StoredMessagesBackend
from ...settings import stored_messages_settings


class RedisBackend(StoredMessagesBackend):
    """

    """
    def __init__(self):
        self.client = redis.StrictRedis(host=stored_messages_settings.REDIS_HOST,
                                        port=stored_messages_settings.REDIS_PORT,
                                        db=stored_messages_settings.REDIS_DB)

    def inbox_list(self, user):
        return self.client.get('user:%d:notifications' % user.pk)

    def inbox_purge(self, user):
        self.client.delete('user:%d:notifications' % user.pk)

    def inbox_get_or_create(self, user, message):
        self.client.sadd('user:%d:notifications' % user.pk, message)

    def create_message(self, user, msg_text, level, extra_tags):
        m = {'message': msg_text, 'level': level, 'tags': extra_tags}
        self.client.sadd('user:%d:archive' % user.pk, m)
        return m

    def archive_list(self, user):
        return self.client.get('user:%d:archive' % user.pk)

    def can_handle(self, msg_instance):
        return (isinstance(msg_instance, dict) and
                msg_instance.keys() == ('message', 'level', 'tags'))
