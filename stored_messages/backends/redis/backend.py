from __future__ import unicode_literals

from django.utils import timezone
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

import json
from collections import namedtuple
import hashlib

from ..exceptions import MessageTypeNotSupported, MessageDoesNotExist
from ..base import StoredMessagesBackend
from .. import signals
from ...settings import stored_messages_settings

try:
    # Let django project bootstrap anyway when not using this backend
    import redis
except ImportError:
    pass


Message = namedtuple('Message', ['id', 'message', 'level', 'tags', 'date', 'url'])


class RedisBackend(StoredMessagesBackend):
    """

    """
    def __init__(self):
        self.client = redis.StrictRedis.from_url(stored_messages_settings.REDIS_URL)

    def _flush(self):
        self.client.flushdb()

    def _toJSON(self, msg_instance):
        """
        Dump a Message instance into a JSON string
        """
        return json.dumps(msg_instance._asdict(), cls=DjangoJSONEncoder)

    def _fromJSON(self, json_msg):
        """
        Return a Message instance built from data contained in a JSON string
        """
        return Message(**json.loads(force_text(json_msg)))

    def _list_key(self, key):
        """
        boilerplate
        """
        ret = []
        for msg_json in self.client.lrange(key, 0, -1):
            ret.append(self._fromJSON(msg_json))
        return ret

    def _list(self, key_tpl, user):
        return self._list_key(key_tpl % user.pk)

    def create_message(self, level, msg_text, extra_tags='', date=None, url=None):
        """
        Message instances are namedtuples of type `Message`.
        The date field is already serialized in datetime.isoformat ECMA-262 format
        """
        if not date:
            now = timezone.now()
        else:
            now = date
        r = now.isoformat()
        if now.microsecond:
            r = r[:23] + r[26:]
        if r.endswith('+00:00'):
            r = r[:-6] + 'Z'

        fingerprint = r + msg_text

        msg_id = hashlib.sha256(fingerprint.encode('ascii', 'ignore')).hexdigest()
        return Message(id=msg_id, message=msg_text, level=level, tags=extra_tags, date=r, url=url)

    def inbox_list(self, user):
        if user.is_anonymous():
            return []
        return self._list('user:%d:notifications', user)

    def inbox_purge(self, user):
        if user.is_authenticated():
            self.client.delete('user:%d:notifications' % user.pk)
            self.client.delete('user:%d:notificationsidx' % user.pk)
            signals.inbox_purged.send(sender=self.__class__, user=user)

    def inbox_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            if self.client.sismember('user:%d:notificationsidx' % user.pk, msg_instance.id):
                return  # a duplicate, NOOP
            else:
                self.client.sadd('user:%d:notificationsidx' % user.pk, msg_instance.id)

            self.client.rpush('user:%d:notifications' % user.pk, self._toJSON(msg_instance))
            signals.inbox_stored.send(sender=self.__class__, user=user, message=msg_instance)

    def inbox_delete(self, user, msg_id):
        for m in self._list('user:%d:notifications', user):
            if m.id == msg_id:
                msg = self.client.lrem('user:%d:notifications' % user.pk, 0, json.dumps(m._asdict()))
                signals.inbox_deleted.send(sender=self.__class__, user=user, message_id=msg_id)
                return msg
        raise MessageDoesNotExist("Message with id %s does not exist" % msg_id)

    def inbox_get(self, user, msg_id):
        for m in self._list('user:%d:notifications', user):
            if m.id == msg_id:
                return m
        raise MessageDoesNotExist("Message with id %s does not exist" % msg_id)

    def archive_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            self.client.rpush('user:%d:archive' % user.pk, self._toJSON(msg_instance))
            signals.archive_stored.send(sender=self.__class__, user=user, message=msg_instance)

    def archive_list(self, user):
        return self._list('user:%d:archive', user)

    def can_handle(self, msg_instance):
        return isinstance(msg_instance, Message)

    def expired_messages_cleanup(self):
        expiration_date = timezone.now() + timezone.timedelta(
            days=-stored_messages_settings.MESSAGE_EXPIRE_DAYS)
        keys = self.client.keys('user:*:notifications')
        for k in keys:
            _, user, _ = k.split(':')
            for m in self._list_key(k):
                if m.date <= expiration_date:
                    msg = json.dumps(m._asdict())
                    self.client.lrem(k, 0, msg)
                    self.client.srem('user:%s:notificationsidx' % user, m.id)
                    self.client.rpop('user:%d:archive' % user, msg)
