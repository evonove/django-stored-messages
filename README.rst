=============================
Django Stored Messages
=============================

.. image:: https://badge.fury.io/py/django-stored-messages.png
    :target: http://badge.fury.io/py/django-stored-messages
    
.. image:: https://travis-ci.org/evonove/django-stored-messages.png?branch=master
        :target: https://travis-ci.org/evonove/django-stored-messages

.. image:: https://coveralls.io/repos/evonove/django-stored-messages/badge.png
        :target: https://coveralls.io/r/evonove/django-stored-messages

.. image:: https://pypip.in/d/django-stored-messages/badge.png
        :target: https://crate.io/packages/django-stored-messages?version=latest


Django contrib.messages on steroids

The app integrates smoothly with Django's [messages framework](http://docs.djangoproject.com/en/dev/ref/contrib/messages/) (`django.contrib.messages`),
but users can decide which messages have to be stored on the database backend and kept available
over sessions.

Documentation
-------------

The full documentation is at http://django-stored-messages.rtfd.org.

Quickstart
----------

Install the app::

    pip install django-stored-messages

Then use it in a project through the django.contrib.messages api::

	import stored_messages
	from django.contrib import messages

    # ok, standard message
	messages.add_message(request, messages.INFO, 'Hello world.')
	# this will be persisted and marked as 'unread'
	messages.add_message(request, stored_messages.STORED_INFO, 'Hello world, going to the database!')

Iterating the messages will automatically mark them as read (but still persisted)::

    storage = messages.get_messages(request)
    for unread_message in storage:
        # unread_message could be a stored message or a "standard" Django message
        do_something_with(unread_message)

...unless you mark the storage as not used::

   storage.used = False

You can mark a stored message as read at any time::

    stored_messages.mark_read(request.user, message)

Features
--------

* Seamless integration with `django.contrib.messages`
* Stored messages are archived in the database
* REST api to retrieve and mark messages as read (needs djangorestframework to be installed)

TODO
----

* Documentation
