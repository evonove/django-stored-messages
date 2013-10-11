from django.test import TestCase, RequestFactory

from stored_messages.compat import get_user_model

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