from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.messages.storage import default_storage

from stored_messages.compat import get_user_model
from stored_messages.models import Inbox, MessageArchive
from stored_messages import add_message, get_messages, STORED_ERROR, DEBUG

import mock


class TestStorage(TestCase):
    urls = 'tests.urls'

    def setUp(self):
        self.user = get_user_model().objects.create_user("test_user", "t@user.com", "123456")
        self.request = RequestFactory().get('/')
        self.request.session = mock.MagicMock()
        self.request.user = self.user

    def test_store(self):
        self.request._messages = default_storage(self.request)
        self.request._messages.level = DEBUG
        add_message(self.request, STORED_ERROR, "an SOS to the world")
        add_message(self.request, DEBUG, "this won't be persisted")
        storage = get_messages(self.request)
        self.assertEqual(len(storage), 2)
        self.assertEqual(MessageArchive.objects.filter(user=self.user).count(), 1)

    def test_store_with_middleware(self):
        self.client.login(username='test_user', password='123456')
        self.client.get('/create')
        inbox_msg = Inbox.objects.filter(user=self.user).count()
        self.assertEqual(inbox_msg, 1)
        self.client.get('/consume')
        self.assertEqual(Inbox.objects.filter(user=self.user).count(), 0)
        self.assertEqual(MessageArchive.objects.filter(user=self.user).count(), 1)

    def test_store_keep_unread(self):
        self.client.login(username='test_user', password='123456')
        self.client.get('/create')
        self.client.get('/consume', data={'keep_storage': True})
        self.assertEqual(Inbox.objects.filter(user=self.user).count(), 1)
        self.assertEqual(MessageArchive.objects.filter(user=self.user).count(), 1)

    def tearDown(self):
        self.user.delete()
