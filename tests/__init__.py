from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.utils.six.moves import reload_module

from stored_messages.compat import get_user_model
from stored_messages import settings
from stored_messages import storage

import mock


class BaseTest(TestCase):
    urls = 'tests.urls'

    def setUp(self):
        self.factory = RequestFactory()

        self.user = get_user_model().objects.create_user("test_user", "t@user.com", "123456")
        self.request = RequestFactory().get('/')
        self.request.session = mock.MagicMock()
        self.request.user = self.user

    def tearDown(self):
        self.user.delete()


class BackendBaseTest(BaseTest):
    """
    Tests that need to access a Backend.
    Given the dynamic nature of Stored Messages settings, retrieving the backend class when we
    need to ovveride settings is a little bit tricky
    """
    def setUp(self):
        reload_module(settings)
        reload_module(storage)
        self.backend = settings.stored_messages_settings.STORAGE_BACKEND()
        super(BackendBaseTest, self).setUp()

    def tearDown(self):
        self.backend._flush()
