from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

import redis
import json

from ..exceptions import MessageTypeNotSupported
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
        ret = []
        for msg_json in self.client.lrange('user:%d:notifications' % user.pk, 0, -1):
            m = json.loads(msg_json)
            ret.append(m)
        return ret

    def inbox_purge(self, user):
        self.client.delete('user:%d:notifications' % user.pk)

    def inbox_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            self.client.rpush('user:%d:notifications' % user.pk,
                              json.dumps(msg_instance, cls=DjangoJSONEncoder))

    def inbox_delete(self, user, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        return self.client.lrem('user:%d:notifications' % user.pk, 0, json.dumps(msg_instance))

    def create_message(self, msg_text, level, extra_tags=''):
        """
        Message instances are plain python dictionaries.
        The date field is already serialized in datetime.isoformat ECMA-262 format
        """
        now = timezone.now()
        r = now.isoformat()
        if now.microsecond:
            r = r[:23] + r[26:]
        if r.endswith('+00:00'):
            r = r[:-6] + 'Z'

        m = {'message': msg_text, 'level': level, 'tags': extra_tags, 'date': r}
        return m

    def archive_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            self.client.rpush('user:%d:archive' % user.pk,
                              json.dumps(msg_instance, cls=DjangoJSONEncoder))

    def archive_list(self, user):
        ret = []
        for msg_json in self.client.lrange('user:%d:archive' % user.pk, 0, -1):
            m = json.loads(msg_json)
            ret.append(m)
        return ret

    def can_handle(self, msg_instance):
        return (isinstance(msg_instance, dict) and
                set(msg_instance.keys()) == {'message', 'level', 'tags', 'date'})
