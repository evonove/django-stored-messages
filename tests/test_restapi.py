from . import BaseTest

from django.core.urlresolvers import reverse

import json

from stored_messages.constants import STORED_ERROR


class TestRESTApi(BaseTest):
    def test_retrieve(self):
        self.client.login(username='test_user', password='123456')
        self.client.get('/create')
        self.client.get('/create')
        r = self.client.get(reverse('stored_messages:inbox-list'))
        messages = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['message']['message'], 'an error')
        self.assertEqual(messages[1]['message']['message'], 'an error')
        self.assertEqual(messages[0]['message']['level'], STORED_ERROR)
        self.assertEqual(messages[1]['message']['level'], STORED_ERROR)

    def test_make_read(self):
        pass