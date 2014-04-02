
class StoredMessagesBackend(object):
    """

    """
    def create_message(self, level, msg_text, extra_tags):
        """
        Create and return a Message instance.
        Instance types depend on the backend implementation.
        """
        raise NotImplementedError()

    def inbox_list(self, user):
        """
        Retrieve all the messages in `user`'s Inbox.
        Return an iterable containing Message instances.
        """
        raise NotImplementedError()

    def inbox_purge(self, user):
        """
        Delete all the messages in `user`'s Inbox.
        Should not return anything.
        """
        raise NotImplementedError()

    def inbox_store(self, users, msg_instance):
        """
        Store a message instance in the inbox for a list
        of users.
        Should not return anything.
        """
        raise NotImplementedError()

    def inbox_delete(self, user, msg_instance):
        """
        Remove a message instance from `user`'s inbox.
        Should not return anything.
        """
        raise NotImplementedError()

    def archive_store(self, users, msg_instance):
        """
        Store a message instance in the archive for a list
        of users.
        Should not return anything.
        """
        raise NotImplementedError()

    def archive_list(self, user):
        """
        Retrieve all the messages in `user`'s archive.
        Return an iterable containing Message instances.
        """
        raise NotImplementedError()

    def can_handle(self, msg_instance):
        """
        Determine if this backend can handle messages
        of the same type of `msg_instance`.
        Return True or False
        """
        raise NotImplementedError()

    def _flush(self):
        """
        Clear all backend data.
        Warning: heavily destructive! Here for convenience, not used by the API anyway.
        """
        raise NotImplementedError()
