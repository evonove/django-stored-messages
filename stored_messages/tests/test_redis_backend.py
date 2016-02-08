from .base import BaseTest

import unittest
import mock

from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from stored_messages.backends.exceptions import MessageTypeNotSupported, MessageDoesNotExist
from stored_messages.backends.redis import RedisBackend
from stored_messages.backends.redis.backend import Message
from stored_messages.backends import signals

from stored_messages import STORED_ERROR


class RedisMock(object):
    """
    Mock the Redis server instance with Django in-memory cache
    """
    def rpush(self, key, data):
        l = cache.get(key)
        if l is None:
            l = []
        l.append(data)
        cache.set(key, l)

    def lrange(self, key, *args, **kwargs):
        return cache.get(key) or []

    def delete(self, key):
        cache.delete(key)

    def lrem(self, key, count, data):
        l = cache.get(key)
        l.remove(data)
        cache.set(key, l)

    def flushdb(self):
        cache.clear()

    def sismember(self, key, val):
        r = cache.get(key)
        return r is not None and val in r

    def sadd(self, key, val):
        l = cache.get(key)

        if l is None:
            l = []

        if val not in l:
            l.append(val)
            cache.set(key, l)

    @staticmethod
    def from_url(*args, **kwargs):
        return RedisMock()

    def StrictRedis(self, *args, **kwargs):
        return self


try:
    from stored_messages.backends.redis.backend import redis
    REDISPY_MISSING = False

    if getattr(settings, 'MOCK_REDIS_SERVER', True):
        patcher = mock.patch('stored_messages.backends.redis.backend.redis')
        redis = patcher.start()  # noqa
        redis.StrictRedis = RedisMock

except ImportError:
    REDISPY_MISSING = True


@unittest.skipIf(REDISPY_MISSING, "redis-py not installed")
class TestRedisBackend(BaseTest):
    def setUp(self):
        super(TestRedisBackend, self).setUp()
        self.client = redis.StrictRedis.from_url(settings.STORED_MESSAGES['REDIS_URL'])
        self.backend = RedisBackend()
        self.backend._flush()
        self.message = self.backend.create_message(STORED_ERROR, 'A message for you')
        self.anon = AnonymousUser()
        self.signals = {}

    def test_inbox_store(self):
        self.backend.inbox_store([self.user], self.message)
        data = self.client.lrange('user:%d:notifications' % self.user.pk, 0, -1).pop()
        self.assertEqual(self.backend._fromJSON(data), self.message)
        self.assertRaises(MessageTypeNotSupported, self.backend.inbox_store, [], {})

    def test_inbox_list(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.backend.inbox_store([self.user], message)
        self.backend.inbox_store([self.user], self.message)
        messages = self.backend.inbox_list(self.user)
        self.assertEqual(messages[0], message)
        self.assertEqual(messages[1], self.message)
        self.assertEqual(self.backend.inbox_list(self.anon), [])

    def test_inbox_purge(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.backend.inbox_store([self.user], self.message)
        self.backend.inbox_store([self.user], message)
        self.backend.inbox_purge(self.user)
        self.assertEqual(len(self.backend.inbox_list(self.user)), 0)
        self.backend.inbox_purge(self.anon)

    def test_inbox_delete(self):
        self.backend.inbox_store([self.user], self.message)
        self.backend.inbox_delete(self.user, self.message.id)
        self.assertEqual(len(self.backend.inbox_list(self.user)), 0)
        self.assertRaises(MessageDoesNotExist, self.backend.inbox_delete, self.user, -1)

    def test_archive_store(self):
        self.backend.archive_store([self.user], self.message)
        data = self.client.lrange('user:%d:archive' % self.user.pk, 0, -1).pop()
        self.assertEqual(self.backend._fromJSON(data), self.message)
        self.assertRaises(MessageTypeNotSupported, self.backend.archive_store, [], {})

    def test_archive_list(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.backend.archive_store([self.user], message)
        self.backend.archive_store([self.user], self.message)
        messages = self.backend.archive_list(self.user)
        self.assertEqual(messages[0], message)
        self.assertEqual(messages[1], self.message)

    def test_create_message(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.assertIsInstance(message, Message)

    def test_inbox_get(self):
        self.backend.inbox_store([self.user], self.message)
        m = self.backend.inbox_get(self.user, self.message.id)
        self.assertEqual(m, self.message)
        self.assertRaises(MessageDoesNotExist, self.backend.inbox_get, self.user, -1)

    def test_can_handle(self):
        self.assertFalse(self.backend.can_handle({}))
        self.assertTrue(self.backend.can_handle(self.message))

    def test_message_expiration(self):
        # start clean
        self.backend._flush()
        six_months_ago = timezone.now() + timezone.timedelta(days=-180)
        self.backend.create_message(STORED_ERROR, 'A message for you', date=six_months_ago)
        self.backend.expired_messages_cleanup()

        keys = self.client.keys('user:*:notifications')
        for k in keys:
            _, user, _ = k.split(':')
            self.assertEqual(self.backend._list_key(k), [])
            self.assertEqual(self.backend._list('user:%s:notifications', user), [])
            self.assertEqual(self.backend._list('user:%s:archive', user), [])

    def test_inbox_signals(self):
        # connect
        signals.inbox_stored.connect(self.inbox_stored)
        signals.inbox_deleted.connect(self.inbox_deleted)
        signals.inbox_purged.connect(self.inbox_purged)

        self.backend.inbox_store([self.user], self.message)
        self.backend.inbox_delete(self.user, self.message.id)
        self.backend.inbox_purge(self.user)

        # disconnect
        signals.inbox_stored.disconnect(self.inbox_stored)
        signals.inbox_deleted.disconnect(self.inbox_deleted)
        signals.inbox_purged.disconnect(self.inbox_purged)

        self.assertIn('inbox_stored', self.signals)
        self.assertIn('inbox_deleted', self.signals)
        self.assertIn('inbox_purged', self.signals)

    def inbox_stored(self, **kwargs):
        self.signals['inbox_stored'] = (kwargs['user'], kwargs['message'])

    def inbox_deleted(self, **kwargs):
        self.signals['inbox_deleted'] = (kwargs['user'], kwargs['message_id'])

    def inbox_purged(self, **kwargs):
        self.signals['inbox_purged'] = (kwargs['user'])

    def test_archive_signals(self):
        # connect
        signals.archive_stored.connect(self.archive_stored)

        self.backend.archive_store([self.user], self.message)

        # disconnect
        signals.archive_stored.disconnect(self.archive_stored)

        self.assertIn('archive_stored', self.signals)

    def archive_stored(self, **kwargs):
        self.signals['archive_stored'] = (kwargs['user'], kwargs['message'])
