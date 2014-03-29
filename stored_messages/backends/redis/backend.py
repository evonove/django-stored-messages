from __future__ import unicode_literals

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

import json

from ..exceptions import MessageTypeNotSupported
from ..base import StoredMessagesBackend
from ...settings import stored_messages_settings


class RedisBackend(StoredMessagesBackend):
    """

    """
    def __init__(self):
        import redis
        self.client = redis.StrictRedis(host=stored_messages_settings.REDIS_HOST,
                                        port=stored_messages_settings.REDIS_PORT,
                                        db=stored_messages_settings.REDIS_DB)

    def _store(self, key_tpl, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            self.client.rpush(key_tpl % user.pk, json.dumps(msg_instance, cls=DjangoJSONEncoder))

    def _list(self, key_tpl, user):
        ret = []
        for msg_json in self.client.lrange(key_tpl % user.pk, 0, -1):
            m = json.loads(msg_json.decode('utf-8'))
            ret.append(m)
        return ret

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

    def inbox_list(self, user):
        return self._list('user:%d:notifications', user)

    def inbox_purge(self, user):
        self.client.delete('user:%d:notifications' % user.pk)

    def inbox_store(self, users, msg_instance):
        self._store('user:%d:notifications', users, msg_instance)

    def inbox_delete(self, user, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        return self.client.lrem('user:%d:notifications' % user.pk, 0, json.dumps(msg_instance))

    def archive_store(self, users, msg_instance):
        self._store('user:%d:archive', users, msg_instance)

    def archive_list(self, user):
        return self._list('user:%d:archive', user)

    def can_handle(self, msg_instance):
        return (isinstance(msg_instance, dict) and
                set(msg_instance.keys()) == {'message', 'level', 'tags', 'date'})
