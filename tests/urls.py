from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^consume', 'tests.views.message_view'),
    url(r'^create', 'tests.views.message_create'),
)
