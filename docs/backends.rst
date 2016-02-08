Storage Backends
================

With version 1.0, the concept of *Storage Backend* was introduced to let developers choose how
messages are persisted. Django Stored Messages provides a pool of backends out of the box and
developers can extend the app providing their own implementation of a *Storage Backend*.

`STORAGE_BACKEND` settings parameter contains a string representing the backend class to use.
If not specified, it defaults to the default backend.

Here follows a list of supported backends.

Default backend: Django ORM
---------------------------

::

    'STORAGE_BACKEND': 'stored_messages.backends.DefaultBackend'

This is the default backend, it stores messages on the configured database using plain old Django
models; it doesn't need any additional configuration.

Redis backend
-------------
::

    'STORAGE_BACKEND': 'stored_messages.backends.redis'

Users' inbox and archives are persisted on a Redis instance. Keys are in the form
`user:<userid>:notifications` `user:<userid>:archive` and values are lists. This backend needs the
`REDIS_URL` settings to be specified, for example::

    STORED_MESSAGES={
        'REDIS_URL': 'redis://username:password@localhost:6379/0',
    }

Implementing your own backend
-----------------------------

Custom backends should derive from ``stored_messages.backends.base.StoredMessagesBackend`` class
and implement all defined methods.
