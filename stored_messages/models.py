from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from .compat import AUTH_USER_MODEL

INBOX_EXPIRE_DAYS = 30  # TODO move to settings


@python_2_unicode_compatible
class Message(models.Model):
    """
    TODO: docstring
    """
    message = models.TextField()
    level = models.IntegerField()
    tags = models.TextField()

    def __str__(self):
        return self.message


@python_2_unicode_compatible
class MessageArchive(models.Model):
    """
    TODO: docstring
    """
    user = models.ForeignKey(AUTH_USER_MODEL)
    message = models.ForeignKey(Message)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "[%s] %s" % (self.user, self.message)


@python_2_unicode_compatible
class Inbox(models.Model):
    """
    TODO: docstring
    """
    user = models.ForeignKey(AUTH_USER_MODEL)
    message = models.ForeignKey(Message)

    def expired(self):
        if INBOX_EXPIRE_DAYS:
            expiration_date = self.message.date + timezone.timedelta(days=INBOX_EXPIRE_DAYS)
            return expiration_date <= timezone.now()
        else:
            return False
    expired.boolean = True  # show a nifty icon in the admin
