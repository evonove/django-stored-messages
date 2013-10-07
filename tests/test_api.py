from . import BaseTest

from stored_messages import mark_read
from stored_messages.models import Inbox


class TestApi(BaseTest):
    def test_mark_as_read(self):
        self.client.login(username='test_user', password='123456')
        self.client.get('/create')
        inbox = Inbox.objects.filter(user=self.user)
        self.assertEqual(len(inbox), 1)
        mark_read(self.user, inbox.get().message)
        self.assertEqual(Inbox.objects.filter(user=self.user).count(), 0)
