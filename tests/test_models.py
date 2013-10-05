from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import timedelta, now
from django.contrib.messages.storage import default_storage

from stored_messages.compat import get_user_model
from stored_messages import add_message, STORED_ERROR
from stored_messages.models import MessageArchive, Inbox

import mock


class TestInbox(TestCase):
    """

    """
    def setUp(self):
        self.user = get_user_model().objects.create_user("test_user", "t@user.com", "123456")
        self.request = RequestFactory().get('/')
        self.request.user = self.user
        self.request.session = mock.MagicMock()
        self.request._messages = default_storage(self.request)

    def test_expire(self):
        add_message(self.request, STORED_ERROR, "an SOS to the world")
        ma = MessageArchive.objects.all()[0]
        ma.message.date = now() - timedelta(days=365)
        ma.message.save()
        inbox = Inbox.objects.create(user=ma.user, message=ma.message)
        self.assertTrue(inbox.expired())

    def tearDown(self):
        self.user.delete()
