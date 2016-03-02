Migrations
==========

``django-stored-messages`` includes Django migrations since version ``1.4.0``. Because you may use this
package since previous versions, it's a good idea following the suggestions below to keep your database in sync
with latest changes. Remember to follow these steps **only if** you're using an earlier ``django-stored-messages``
version and you've already executed your own migrations.

Migrate from 1.3.x to 1.4.0
---------------------------

Version ``1.3.x`` already has models and changes of ``1.4.0``. For this reason, all migrations should be
faked.

* update ``django-stored-messages`` to version ``1.4.0`` (remember to check the compatibility table)
* from your project root folder, run::

    $ python manage.py migrate stored_messages 0002 --fake


Migrate from 1.2.0 (or earlier) to 1.4.0
--------------------------------------

Version ``1.2.0.`` (or earlier) has all models except the ``url`` field introduced in the ``Message`` model.
For this reason the initial migration should be faked, while the second should be executed.

* update ``django-stored-messages`` to version ``1.4.0`` (remember to check the compatibility table)
* from your project root folder, run::

    $ python manage.py migrate stored_messages 0001 --fake

* as last step, launch the missing migration::

    $ python manage.py migrate stored_messages
