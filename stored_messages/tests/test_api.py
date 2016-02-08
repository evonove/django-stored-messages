# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .base import BaseTest

from django.contrib.auth import get_user_model
from django.utils import timezone

from stored_messages import mark_read, add_message_for, broadcast_message, mark_all_read
from stored_messages.models import Inbox, MessageArchive
from stored_messages.backends.exceptions import MessageDoesNotExist
import stored_messages


class TestApi(BaseTest):
    def test_mark_as_read(self):
        self.client.login(username='test_user', password='123456')
        self.client.get('/create')
        inbox = Inbox.objects.filter(user=self.user)
        self.assertEqual(len(inbox), 1)
        mark_read(self.user, inbox.get().message)
        self.assertEqual(Inbox.objects.filter(user=self.user).count(), 0)

    def test_mark_as_read_idempotent(self):
        self.client.login(username='test_user', password='123456')
        self.client.get('/create')
        msg_archive = MessageArchive.objects.filter(user=self.user).get()
        mark_read(self.user, msg_archive.message)
        self.assertRaises(MessageDoesNotExist, mark_read, self.user, msg_archive.message)

    def test_add_message_for(self):
        now = timezone.now() + timezone.timedelta(days=-1)
        url = 'http://example.com/error'

        user2 = get_user_model().objects.create_user("another_user", "u@user.com", "123456")
        add_message_for([user2, self.user], stored_messages.STORED_ERROR, 'Multiple errors', 'extra', now, url)
        self.assertEqual(Inbox.objects.count(), 2)
        self.assertEqual(MessageArchive.objects.count(), 2)

        self.assertEqual(Inbox.objects.get(user=user2.id).message.tags, 'extra')
        self.assertEqual(Inbox.objects.get(user=self.user).message.tags, 'extra')

        self.assertEqual(Inbox.objects.get(user=user2.id).message.date, now)
        self.assertEqual(Inbox.objects.get(user=self.user).message.date, now)

        self.assertEqual(Inbox.objects.get(user=user2.id).message.url, url)
        self.assertEqual(Inbox.objects.get(user=self.user).message.url, url)

        self.assertEqual(Inbox.objects.get(user=user2.id).message.message, "Multiple errors")
        self.assertEqual(Inbox.objects.get(user=self.user).message.message, "Multiple errors")

        self.assertEqual(MessageArchive.objects.get(user=user2.id).message.message,
                         "Multiple errors")
        self.assertEqual(MessageArchive.objects.get(user=self.user).message.message,
                         "Multiple errors")

    def test_broadcast_message(self):
        user1 = get_user_model().objects.create_user("user1", "u1@user.com", "123456")
        user2 = get_user_model().objects.create_user("user2", "u2@user.com", "123456")
        user3 = get_user_model().objects.create_user("user3", "u3@user.com", "123456")

        now = timezone.now() + timezone.timedelta(days=-1)
        url = 'http://example.com/error'
        broadcast_message(stored_messages.STORED_INFO, 'broadcast test message', 'extra', now, url)
        self.assertEqual(Inbox.objects.get(user=user1.id).message.message, "broadcast test message")
        self.assertEqual(Inbox.objects.get(user=user2.id).message.message, "broadcast test message")
        self.assertEqual(Inbox.objects.get(user=user3.id).message.message, "broadcast test message")

        self.assertEqual(Inbox.objects.get(user=user1.id).message.tags, 'extra')
        self.assertEqual(Inbox.objects.get(user=user2.id).message.tags, 'extra')
        self.assertEqual(Inbox.objects.get(user=user3.id).message.tags, 'extra')

        self.assertEqual(Inbox.objects.get(user=user1.id).message.date, now)
        self.assertEqual(Inbox.objects.get(user=user2.id).message.date, now)
        self.assertEqual(Inbox.objects.get(user=user3.id).message.date, now)

        self.assertEqual(Inbox.objects.get(user=user1.id).message.url, url)
        self.assertEqual(Inbox.objects.get(user=user2.id).message.url, url)
        self.assertEqual(Inbox.objects.get(user=user3.id).message.url, url)

        self.assertEqual(MessageArchive.objects.get(user=user1.id).message.message,
                         "broadcast test message")
        self.assertEqual(MessageArchive.objects.get(user=user2.id).message.message,
                         "broadcast test message")
        self.assertEqual(MessageArchive.objects.get(user=user3.id).message.message,
                         "broadcast test message")

    def test_mark_all_read(self):
        for i in range(20):
            stored_messages.add_message_for([self.user], stored_messages.INFO, "unicode message ❤")
        inbox = Inbox.objects.filter(user=self.user)
        self.assertEqual(len(inbox), 20)
        mark_all_read(self.user)
        self.assertEqual(Inbox.objects.filter(user=self.user).count(), 0)
