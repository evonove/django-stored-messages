
class StoredMessagesBackend(object):
    """

    """
    def create_message(self, level, msg_text, extra_tags, date=None):
        """
        Create and return a `Message` instance.
        Instance types depend on backends implementation.

        Params:
            `level`: message level (see django.contrib.messages)
            `msg_text`: what you think it is
            `extra_tags`: see django.contrib.messages
            `date`: a DateTime (optional)

        Return:
            `Message` instance
        """
        raise NotImplementedError()

    def inbox_list(self, user):
        """
        Retrieve all the messages in `user`'s Inbox.

        Params:
            `user`: Django User instance

        Return:
            An iterable containing `Message` instances
        """
        raise NotImplementedError()

    def inbox_purge(self, user):
        """
        Delete all the messages in `user`'s Inbox.

        Params:
            user: Django User instance

        Return:
            None
        """
        raise NotImplementedError()

    def inbox_store(self, users, msg_instance):
        """
        Store a `Message` instance in the inbox for a list
        of users.

        Params:
            users: a list or iterable containing Django User instances
            msg_instance: Message instance to persist in inbox

        Return:
            None

        Raise:
            MessageTypeNotSupported if `msg_instance` cannot be managed by current backend
        """
        raise NotImplementedError()

    def inbox_delete(self, user, msg_id):
        """
        Remove a `Message` instance from `user`'s inbox.

        Params:
            user: Django User instance
            msg_id: Message identifier

        Return:
            None

        Raise:
            MessageDoesNotExist if msg_id was not found
        """
        raise NotImplementedError()

    def inbox_get(self, user, msg_id):
        """
        Retrieve a `Message` instance from `user`'s inbox.

        Params:
            user: Django User instance
            msg_id: Message identifier

        Return:
            A `Message` instance

        Raise:
            MessageDoesNotExist if msg_id was not found
        """

    def archive_store(self, users, msg_instance):
        """
        Store a `Message` instance in the archive for a list
        of users.

        Params:
            users: a list or iterable containing Django User instances
            msg_instance: Message instance to persist in archive

        Return:
            None

        Raise:
            MessageTypeNotSupported if `msg_instance` cannot be managed by current backend
        """
        raise NotImplementedError()

    def archive_list(self, user):
        """
        Retrieve all the messages in `user`'s archive.

        Params:
            user: Django User instance

        Return:
            An iterable containing `Message` instances
        """
        raise NotImplementedError()

    def can_handle(self, msg_instance):
        """
        Determine if this backend can handle messages
        of the same type of `msg_instance`.

        Params:
            `msg_instance`: `Message` instance

        Return:
            True if type is correct, False otherwise
        """
        raise NotImplementedError()

    def expired_messages_cleanup(self):
        """
        Remove messages that have been expired.

        Params:
            None

        Return:
           None
        """
        raise NotImplementedError()

    def _flush(self):
        """
        Clear all backend data.
        Warning: heavily destructive! Here for convenience, not used by the API anyway.

        Params:
            None

        Return:
            None
        """
        raise NotImplementedError()
