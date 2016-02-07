Django Stored Messages
======================

.. image:: https://badge.fury.io/py/django-stored-messages.png
    :target: http://badge.fury.io/py/django-stored-messages

.. image:: https://travis-ci.org/evonove/django-stored-messages.png?branch=master
        :target: https://travis-ci.org/evonove/django-stored-messages

.. image:: https://coveralls.io/repos/evonove/django-stored-messages/badge.png
        :target: https://coveralls.io/r/evonove/django-stored-messages


Django contrib.messages on steroids

The app integrates smoothly with Django's `messages framework <http://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_
(``django.contrib.messages``), but users can decide which messages have to be stored on the database
backend and kept available over sessions.

Features
--------

* Seamless integration with ``django.contrib.messages``
* All the features are in a mixin you can attach to your existing storage
* Stored messages are archived in the database or in a Redis instance
* Users can configure which message levels have to be persisted
* REST api to retrieve and mark messages as read (needs ``djangorestframework``)
* Signalling api to perform actions in response to messages activity

Compatibility table
-------------------

* Python 2.7, 3.4
* Django 1.4, 1.5, 1.6, 1.7, 1.8
* Django Rest Framework 2.4.x, 3.1.x (only if you want to use REST endpoints)

Documentation
-------------

The full documentation is at http://django-stored-messages.rtfd.org.

Quickstart
----------

Follow instruction for firing up `django.contrib.messages <http://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_,
then install the app::

    pip install django-stored-messages

Add it to the installed apps::

    INSTALLED_APPS = (
        # ...
        'stored_messages',
    )

In the settings, tell Django which is the message storage::

    MESSAGE_STORAGE = 'stored_messages.storage.PersistentStorage'

Then use it in a project through the django.contrib.messages api. The app provides for convenience
some message levels which are persisted by default::

    import stored_messages
    from django.contrib import messages

    # standard message
    messages.add_message(request, messages.INFO, 'Hello world.')
    # this will be persisted and marked as 'unread'
    messages.add_message(request, stored_messages.STORED_INFO, 'Hello world, to the database!')

stored_messages expose the same api as well, so one can do::

    import stored_messages
    stored_messages.add_message(request, stored_messages.INFO, 'Hello!')

If you want to use standard message levels but persist the messages, just add something like this
to the settings::

    from django.contrib import messages
    STORED_MESSAGES = {
        # persist standard infos and standard errors
        'STORE_LEVELS': (messages.INFO, messages.ERROR,),
    }

Iterating the messages will automatically mark them as read (but still persisted)::

    storage = messages.get_messages(request)
    for unread_message in storage:
        # unread_message could be a stored message or a "standard" Django message
        do_something_with(unread_message)

...unless you mark the storage as not used::

   storage.used = False

You can mark a stored message as read at any time::

    stored_messages.mark_read(request.user, message)

Want to store your messages on Redis instead of your database? Here you go::

    STORED_MESSAGES = {
        'STORAGE_BACKEND': 'stored_messages.backends.RedisBackend',
        'REDIS_URL': 'redis://localhost:6379/0',
    }

Examples
--------

`GitHub-like notifications with Stored Messages and AngularJS <http://dev.pippi.im/2013/10/22/build-github-like-notifications-with-django-messages-and-angular-js/>`_
