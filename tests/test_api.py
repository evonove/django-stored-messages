from . import BaseTest

from stored_messages import mark_read
from stored_messages.models import Inbox, MessageArchive


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
        msg = MessageArchive.objects.filter(user=self.user).get()
        self.assertTrue(mark_read(self.user, msg))
        self.assertFalse(mark_read(self.user, msg))
