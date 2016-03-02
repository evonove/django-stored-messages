.. complexity documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-stored-messages's documentation!
==================================================

Django contrib.messages on steroids!

The app integrates smoothly with Django's `messages framework <http://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_
(``django.contrib.messages``), but users can decide which messages have to be stored on the database
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

* Python 2.7, 3.4, 3.5
* Django 1.8, 1.9
* Django Rest Framework >= 3.3 (only if you want to use REST endpoints)

Do you use an earlier version of Django or Django Rest Framework? An `old version of stored_messages`_ is available even
if it's **not supported anymore**. Anyway, plan a migration to a newer version.

.. _old version of stored_messages: https://github.com/evonove/django-stored-messages/tree/1.3.1

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   backends
   advanced_usage
   migrations
   contributing
   authors
   history
