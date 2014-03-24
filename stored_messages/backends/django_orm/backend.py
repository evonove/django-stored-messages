from ..base import StoredMessagesBackend

from ...models import Inbox


class DjangoOrmBackend(StoredMessagesBackend):
    """

    """
    def get_inbox(self, user):
        return Inbox.objects.filter(user=user).select_related("message")
