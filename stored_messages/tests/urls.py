from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^consume$', 'stored_messages.tests.views.message_view'),
    url(r'^create$', 'stored_messages.tests.views.message_create'),
    url(r'^create_mixed$', 'stored_messages.tests.views.message_create_mixed'),
    url(r'^messages', include('stored_messages.urls', namespace='stored_messages'))
)
