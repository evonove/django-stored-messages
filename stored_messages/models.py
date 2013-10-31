from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .compat import AUTH_USER_MODEL
from .settings import stored_messages_settings


@python_2_unicode_compatible
class Message(models.Model):
    """
    TODO: docstring
    """
    message = models.TextField()
    level = models.IntegerField()
    tags = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


@python_2_unicode_compatible
class MessageArchive(models.Model):
    """
    TODO: docstring
    """
    user = models.ForeignKey(AUTH_USER_MODEL)
    message = models.ForeignKey(Message)

    def __str__(self):
        return "[%s] %s" % (self.user, self.message)


@python_2_unicode_compatible
class Inbox(models.Model):
    """
    TODO: docstring
    """
    user = models.ForeignKey(AUTH_USER_MODEL)
    message = models.ForeignKey(Message)

    class Meta:
        verbose_name_plural = _('inboxes')

    def expired(self):
        expiration_date = self.message.date + timezone.timedelta(
            days=stored_messages_settings.INBOX_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    expired.boolean = True  # show a nifty icon in the admin

    def __str__(self):
        return "[%s] %s" % (self.user, self.message)
