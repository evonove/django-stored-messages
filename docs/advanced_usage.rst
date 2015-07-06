Advanced Usage
==============

Interact with stored messages through the REST api
--------------------------------------------------

When *Django REST framework* is available and installed, Stored Messages exposes a RESTful api
which consists of the following endpoints:

 * `/inbox/` - method: `GET`: retrieve the list of unread messages for current logged in user.
 * `/inbox/{lookup}/` - method: `GET`: get the details for the message having `{lookup}` pk.
 * `/inbox/{lookup}/read/` - method: `POST`: mark the message having `{lookup}` pk as read.
 * `/mark_all_read/` - method: `POST`: mark all messages as read for current logged in user.


Writing a custom storage
------------------------

All the functionalities for persisitng messages are implemented in the `StorageMixin` class. Such
mixin can be derived together with one of the default storages provided by `django.contrib.messages`
so that messages which types are configured to be persisted will be actually saved to the database
and all the others will be passed to the default storage. The mixin could also be implemented
together with a more specialized storage provided by the user and not necessarily one of those
provided by Django.


Signals
-------

A few hooks are available in `backends.signals`.

For inbox we raise the following signals:

* `inbox_stored`: a message has been stored, providing `user` and `message` as arguments
* `inbox_deleted`: a message has been deleted, providing `user` and `message_id` as arguments
* `inbox_purged`: the inbox has been purged, providing `user` as argument

For archive we raise the following signals:

* `archive_stored`: a message has been stored, providing `user` and `message` as arguments
