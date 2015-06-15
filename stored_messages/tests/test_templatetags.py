# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.template import RequestContext, Template

from .base import BaseTest

import stored_messages


class TestStoredMessagesTags(BaseTest):
    def _create_messages(self):
        # create a message
        for i in range(20):
            stored_messages.add_message_for([self.user], stored_messages.INFO, "unicode message ❤")

    def test_stored_messages_list(self):
        self._create_messages()

        t = Template("{% load stored_messages_tags %}"
                     "{% stored_messages_list 15 %}")
        render = t.render(RequestContext(self.request))
        self.assertInHTML("<li>[test_user] unicode message ❤</li>", render, 15)

    def test_stored_messages_archive(self):
        self._create_messages()

        t = Template("{% load stored_messages_tags %}"
                     "{% stored_messages_archive 15 %}")
        render = t.render(RequestContext(self.request))
        self.assertInHTML("<li>[test_user] unicode message ❤</li>", render, 15)

    def test_stored_messages_count(self):
        self._create_messages()

        t = Template("{% load stored_messages_tags %}"
                     "{% stored_messages_count as count %}"
                     "<p>There are {{ count }} messages</p>")
        render = t.render(RequestContext(self.request))
        self.assertInHTML("<p>There are 20 messages</p>", render, 1)

    def test_stored_messages_list_empty_for_unauthenticated_user(self):
        stored_messages.add_message_for([self.user], stored_messages.INFO, "unicode message ❤")

        t = Template("{% load stored_messages_tags %}"
                     "{% stored_messages_list 15 %}")
        render = t.render(RequestContext(self.factory.get("/")))

        self.assertInHTML("<li>[test_user] unicode message ❤</li>", render, 0)

    def test_stored_messages_archive_empty_for_unauthenticated_user(self):
        stored_messages.add_message_for([self.user], stored_messages.INFO, "unicode message ❤")

        t = Template("{% load stored_messages_tags %}"
                     "{% stored_messages_archive 15 %}")
        render = t.render(RequestContext(self.factory.get("/")))

        self.assertInHTML("<li>[test_user] unicode message ❤</li>", render, 0)

    def assertInHTML(self, needle, haystack, count=None, msg_prefix=''):
        import django
        if django.VERSION < (1, 5):
            real_count = haystack.count(needle)
            return self.assertEqual(real_count, count)
        else:
            return super(TestStoredMessagesTags, self).assertInHTML(
                needle, haystack, count, msg_prefix)
