from django.http import HttpResponse
from django.contrib import messages


def message_view(request):
    keep_storage = request.GET.get('keep_storage', False)
    storage = messages.get_messages(request)
    for message in storage:
        pass
    if keep_storage:
        storage.used = False
    return HttpResponse()


def message_create(request):
    messages.add_message(request, messages.ERROR, "an error")
    messages.add_message(request, messages.DEBUG, "a debug message")
    return HttpResponse()
