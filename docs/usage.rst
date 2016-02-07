Usage
=====

Using django.contrib.messages api
---------------------------------

Which messages are stored?
##########################

django-stored-messages integrates smoothly with `django.contrib.messages` so you can keep on adding
flash messages together with stored ones. But how does django-stored-messages know which messages
have to be persisted and which not? This is completely up to the user, who can configure the
desired behaviour through the `STORE_LEVELS` settings. This setting is a list containing the
message levels (both provided by Django or custom) which have to be persisted. For example::

    'STORE_LEVELS': (
        INFO,
        ERROR,
    ),

tells django-stored-messages to persist messages of level `INFO` and `ERROR`, both provided by
Django. django-stored-messages provides a set of message levels for convenience that can be used
to store message without setting anything and letting Django levels to behave normally:

    * STORED_DEBUG,
    * STORED_INFO,
    * STORED_SUCCESS,
    * STORED_WARNING,
    * STORED_ERROR,

How do I retrieve stored messages?
##################################

Premise: stored messages have a status which can be `read` or `unread`. Using the Django api for
displaying messages, it will show `unread` messages together with Django "regular" messages.
For example, in a template::

    {% if messages %}
    <ul class="messages">
        {% for message in messages %}
        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}

Please notice that displaying stored messages, just like regular messages, will expire them: this
means regular messages are removed from their storages (cookies or the session) and stored messages
will be marked as `read` (they'll be still in the database, though).
If this is not the desired behaviour, and you want to keep messages `unread` even after displaying
them, set the `used` parameter in the storage instance as `False`::

    storage = messages.get_messages(request)
    for message in storage:
        do_something_with(message)
    storage.used = False


Using django-stored-messages api
--------------------------------

There are situations in which one can leverage the fact that messages are stored in the database
and use them beyond the intentions of `django.contrib.messages.api`. For example one could:

    * send a message without having access to a request object
    * send a message to multiple users
    * manually mark a message `read` instead of doing this automatically iterating the storage

django-stored-messages provides an additional api containing some utility methods useful in such
cases.

.. automodule:: stored_messages.api
   :members:
