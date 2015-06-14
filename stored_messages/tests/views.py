# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

import stored_messages


def message_view(request):
    keep_storage = request.GET.get('keep_storage', False)
    storage = stored_messages.get_messages(request)
    for _ in storage:
        pass
    if keep_storage:
        storage.used = False
    return HttpResponse()


def message_create(request):
    stored_messages.add_message(request, stored_messages.STORED_ERROR, "an error ☢")
    stored_messages.add_message(request, stored_messages.STORED_DEBUG, "a debug message ☢")
    return HttpResponse()


def message_create_mixed(request):
    stored_messages.add_message(request, stored_messages.STORED_ERROR, "an error ☢")
    stored_messages.add_message(request, stored_messages.ERROR, "an error not persisted ☢")
    return HttpResponse()
