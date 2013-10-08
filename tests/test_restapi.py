from . import BaseTest

from django.core.urlresolvers import reverse
from unittest import skipUnless

import json

from stored_messages.constants import STORED_ERROR

try:
    import rest_framework
    rest_framework_installed = True
except ImportError:
    rest_framework_installed = False


class TestRESTApi(BaseTest):
    @skipUnless(rest_framework_installed, "Django restframework is not installed")
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

    @skipUnless(rest_framework_installed, "Django restframework is not installed")
    def test_make_read(self):
        self.client.login(username='test_user', password='123456')
        self.client.get('/create')
        r = self.client.get(reverse('stored_messages:inbox-list'))
        messages = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(messages), 1)
        msg_id = messages[0]['message']['id']
        r = self.client.post(reverse('stored_messages:inbox-read', args=(msg_id,)))
        self.assertEqual(r.status_code, 200)
        r = self.client.get(reverse('stored_messages:inbox-list'))
        messages = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(messages), 0)
