from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^consume$', 'tests.views.message_view'),
    url(r'^create$', 'tests.views.message_create'),
    url(r'^create_mixed$', 'tests.views.message_create_mixed'),
    url(r'^messages', include('stored_messages.urls', namespace='stored_messages'))
)
