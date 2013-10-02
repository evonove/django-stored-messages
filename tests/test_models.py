#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.messages import add_message, ERROR, get_messages
from django.contrib.messages.storage import default_storage

from stored_messages import models


class TestMessage(TestCase):
    """

    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_something(self):
        request = self.factory.get('/')
        request._messages = default_storage(request)
        add_message(request, ERROR, 'here iam')
        storage = get_messages(request)
        for message in storage:
            pass

    def tearDown(self):
        pass