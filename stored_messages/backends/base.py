
class StoredMessagesBackend(object):
    """

    """
    def inbox_list(self, user):
        """
        Retrieve all the messages in `user`'s Inbox
        """
        raise NotImplementedError

    def inbox_purge(self, user):
        """
        Delete all the messages in `user`'s Inbox
        """
        raise NotImplementedError

    def inbox_get_or_create(self, user, msg_text):
        """
        Create or retrieve an `user`'s Inbox entry containing `msg_text`
        """
        raise NotImplementedError

    def create_message(self, user, level, msg_text, extra_tags):
        """
        Create a Message instance
        """
        raise NotImplementedError

    def archive_list(self, user):
        """
        Retrieve all the messages in `user`'s archive
        """
        raise NotImplementedError

    def can_handle(self, msg_instance):
        """
        Determine if this backend can handle message of type `msg_instance`
        """
        raise NotImplementedError
