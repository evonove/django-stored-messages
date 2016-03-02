============
Installation
============

At the command line::

    $ easy_install django-stored-messages

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv django-stored-messages
    $ pip install django-stored-messages

Add `stored_messages` to the list of installed apps. You also have to enable
`django.contrib.messages` framework for using stored messages::

    INSTALLED_APPS = (
        # ...
        'django.contrib.messages',
        'stored_messages',
    )

    MIDDLEWARE_CLASSES = (
        # ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'django.contrib.messages.context_processors.messages'
    )

Specify which is the storage class for messages, django-stored-messages provides a convenient
default which adds persistent messages to the `storage.fallback.FallbackStorage` class from Django::

    MESSAGE_STORAGE = 'stored_messages.storage.PersistentStorage'

As last step, don't forget to run Django migrations::

    $ python manage.py migrate
