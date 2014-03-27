from . import BaseTest

import json

from stored_messages.backends.exceptions import MessageTypeNotSupported
from stored_messages.backends.redis import RedisBackend
from stored_messages import STORED_ERROR
from stored_messages.settings import stored_messages_settings


class TestRedisBackend(BaseTest):
    def setUp(self):
        import redis

        super(TestRedisBackend, self).setUp()
        self.client = redis.StrictRedis(host=stored_messages_settings.REDIS_HOST,
                                        port=stored_messages_settings.REDIS_PORT,
                                        db=stored_messages_settings.REDIS_DB)
        self.backend = RedisBackend()
        self.message = self.backend.create_message('A message for you', STORED_ERROR)

    def tearDown(self):
        self.client.delete('user:%d:notifications' % self.user.pk)
        self.client.delete('user:%d:archive' % self.user.pk)

    def _same_message(self, one, other):
        same = True
        try:
            for k, v in one.items():
                same &= other[k] == v
            return same
        except KeyError:
            return False

    def test_can_handle(self):
        self.assertTrue(self.backend.can_handle(self.message))
        self.message['foo'] = 'bar'
        self.assertFalse(self.backend.can_handle(self.message))

    def test_inbox_store(self):
        self.backend.inbox_store([self.user], self.message)
        data = self.client.lrange('user:%d:notifications' % self.user.pk, 0, -1).pop()
        self.assertTrue(self._same_message(json.loads(data), self.message))
        self.assertRaises(MessageTypeNotSupported, self.backend.inbox_store, [], {})

    def test_inbox_list(self):
        message = self.backend.create_message('Another message for you', STORED_ERROR)
        self.backend.inbox_store([self.user], message)
        self.backend.inbox_store([self.user], self.message)
        messages = self.backend.inbox_list(self.user)
        self.assertTrue(self._same_message(messages[0], message))
        self.assertTrue(self._same_message(messages[1], self.message))

    def test_inbox_purge(self):
        message = self.backend.create_message('Another message for you', STORED_ERROR)
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
        self.assertTrue(self._same_message(json.loads(data), self.message))
        self.assertRaises(MessageTypeNotSupported, self.backend.archive_store, [], {})

    def test_archive_list(self):
        message = self.backend.create_message('Another message for you', STORED_ERROR)
        self.backend.archive_store([self.user], message)
        self.backend.archive_store([self.user], self.message)
        messages = self.backend.archive_list(self.user)
        self.assertTrue(self._same_message(messages[0], message))
        self.assertTrue(self._same_message(messages[1], self.message))