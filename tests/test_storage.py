from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.messages import add_message, get_messages, ERROR, DEBUG
from django.contrib.messages.storage import default_storage

from stored_messages.compat import get_user_model
from stored_messages.models import Inbox

import mock


class TestStorage(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user', password='123456')
        self.request = RequestFactory().get('/')
        self.request.session = mock.MagicMock()
        self.request.user = self.user

    def test_store(self):
        self.request._messages = default_storage(self.request)
        self.request._messages.level = DEBUG
        add_message(self.request, ERROR, 'an SOS to the world')
        add_message(self.request, DEBUG, "this won't be persisted")
        storage = get_messages(self.request)
        self.assertEqual(len(storage), 2)
        inbox_msg = Inbox.objects.filter(user=self.user).count()
        self.assertEqual(inbox_msg, 1)
