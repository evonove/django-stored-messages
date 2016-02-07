.. complexity documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-stored-messages's documentation!
=================================================================

Django contrib.messages on steroids!

The app integrates smoothly with Django's `messages framework <http://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_
(`django.contrib.messages`), but users can decide which messages have to be stored on the database
backend and kept available over sessions.

Features
--------

* Seamless integration with ``django.contrib.messages``
* All the features are in a mixin you can attach to your existing storage
* Stored messages are archived in the database or in a Redis instance
* Users can configure which message levels have to be persisted
* REST api to retrieve and mark messages as read (needs ``djangorestframework`` being installed)
* Signalling api to perform actions in response to messages activity

Compatibility table
-------------------

* Python 2.7, 3.4
* Django 1.4, 1.5, 1.6, 1.7, 1.8
* Django Rest Framework 2.4.x, 3.1.x (only if you want to use REST endpoints)

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   backends
   advanced_usage
   contributing
   authors
   history
