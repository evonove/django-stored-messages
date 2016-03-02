from django.contrib import admin
from django.conf.urls import url, include

from stored_messages.tests.views import message_view, message_create, message_create_mixed


admin.autodiscover()

urlpatterns = [
    url(r'^consume$', message_view),
    url(r'^create$', message_create),
    url(r'^create_mixed$', message_create_mixed),
    url(r'^messages', include('stored_messages.urls', namespace='stored_messages'))
]
