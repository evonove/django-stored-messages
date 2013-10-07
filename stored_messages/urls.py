from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'inbox', views.InboxViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
