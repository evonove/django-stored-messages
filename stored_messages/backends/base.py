
class StoredMessagesBackend(object):
    """

    """
    def create_message(self, level, msg_text, extra_tags):
        """
        Create and return a Message instance
        """
        raise NotImplementedError

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

    def inbox_store(self, users, msg_instance):
        """
        Store a message instance in the inbox for a list
        of users
        """
        raise NotImplementedError

    def inbox_delete(self, user, msg_instance):
        """
        Remove a message instance from `user`'s inbox
        """
        raise NotImplementedError

    def archive_store(self, users, msg_instance):
        """
        Store a message instance in the archive for a list
        of users
        """
        raise NotImplementedError

    def archive_list(self, user):
        """
        Retrieve all the messages in `user`'s archive
        """
        raise NotImplementedError

    def can_handle(self, msg_instance):
        """
        Determine if this backend can handle messages
        of type `msg_instance`
        """
        raise NotImplementedError
