from . import BaseTest

import unittest
import mock

from django.conf import settings
from django.core.cache import cache

from stored_messages.backends.exceptions import MessageTypeNotSupported
from stored_messages.backends.redis import RedisBackend

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
        redis = patcher.start()
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

    def tearDown(self):
        self.client.delete('user:%d:notifications' % self.user.pk)
        self.client.delete('user:%d:archive' % self.user.pk)

    def _same_message(self, one, other):
        if one != other:
            print one,other
        return one == other

    def _test_can_handle(self):
        self.assertTrue(self.backend.can_handle(self.message))
        self.message['foo'] = 'bar'
        self.assertFalse(self.backend.can_handle(self.message))

    def test_inbox_store(self):
        self.backend.inbox_store([self.user], self.message)
        data = self.client.lrange('user:%d:notifications' % self.user.pk, 0, -1).pop()
        self.assertTrue(self._same_message(self.backend._fromJSON(data), self.message))
        self.assertRaises(MessageTypeNotSupported, self.backend.inbox_store, [], {})

    def test_inbox_list(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.backend.inbox_store([self.user], message)
        self.backend.inbox_store([self.user], self.message)
        messages = self.backend.inbox_list(self.user)
        self.assertTrue(self._same_message(messages[0], message))
        self.assertTrue(self._same_message(messages[1], self.message))

    def test_inbox_purge(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.backend.inbox_store([self.user], self.message)
        self.backend.inbox_store([self.user], message)
        self.backend.inbox_purge(self.user)
        self.assertEqual(len(self.backend.inbox_list(self.user)), 0)

    def test_inbox_delete(self):
        self.backend.inbox_store([self.user], self.message)
        self.backend.inbox_delete(self.user, self.message)
        self.assertEqual(len(self.backend.inbox_list(self.user)), 0)
        self.assertRaises(MessageTypeNotSupported, self.backend.inbox_delete, self.user, {})

    def test_archive_store(self):
        self.backend.archive_store([self.user], self.message)
        data = self.client.lrange('user:%d:archive' % self.user.pk, 0, -1).pop()
        self.assertTrue(self._same_message(self.backend._fromJSON(data), self.message))
        self.assertRaises(MessageTypeNotSupported, self.backend.archive_store, [], {})

    def test_archive_list(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.backend.archive_store([self.user], message)
        self.backend.archive_store([self.user], self.message)
        messages = self.backend.archive_list(self.user)
        self.assertTrue(self._same_message(messages[0], message))
        self.assertTrue(self._same_message(messages[1], self.message))
