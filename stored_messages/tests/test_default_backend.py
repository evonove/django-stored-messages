# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import BaseTest

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from stored_messages.backends.exceptions import MessageTypeNotSupported, MessageDoesNotExist
from stored_messages.backends.default import DefaultBackend
from stored_messages.models import Message, Inbox, MessageArchive
from stored_messages import STORED_ERROR


class TestDefaultBackend(BaseTest):
    def setUp(self):
        super(TestDefaultBackend, self).setUp()
        self.backend = DefaultBackend()
        self.message = self.backend.create_message(STORED_ERROR, 'A message for you ♡')
        self.anon = AnonymousUser()

    def test_inbox_store(self):
        self.backend.inbox_store([self.user], self.message)
        m = Inbox.objects.filter(user=self.user).get()
        self.assertEqual(m.message, self.message)
        self.assertRaises(MessageTypeNotSupported, self.backend.inbox_store, [], {})

    def test_inbox_list(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you ♡♡♡')
        self.backend.inbox_store([self.user], message)
        self.backend.inbox_store([self.user], self.message)
        messages = self.backend.inbox_list(self.user)
        self.assertEqual(messages[0], message)
        self.assertEqual(messages[1], self.message)
        self.assertEqual(len(self.backend.inbox_list(self.anon)), 0)

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
        m = MessageArchive.objects.filter(user=self.user).all()[0]
        self.assertEqual(m.message, self.message)
        self.assertRaises(MessageTypeNotSupported, self.backend.archive_store, [], {})

    def test_archive_list(self):
        message = self.backend.create_message(STORED_ERROR, 'Another message for you')
        self.backend.archive_store([self.user], message)
        self.backend.archive_store([self.user], self.message)
        messages = self.backend.archive_list(self.user)
        self.assertEqual(messages[0].message, message)
        self.assertEqual(messages[1].message, self.message)

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
        six_months_ago = timezone.now() + timezone.timedelta(days=-180)
        self.message.date = six_months_ago
        self.message.save()
        self.backend.expired_messages_cleanup()

        n_archives = MessageArchive.objects.count()
        n_inbox = Inbox.objects.count()
        n_messages = Message.objects.count()
        self.assertEqual(n_archives, 0)
        self.assertEqual(n_inbox, 0)
        self.assertEqual(n_messages, 0)
