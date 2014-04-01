"""
This module is largely inspired by django-rest-framework settings.

Settings for the Stored Messages framework are all namespaced in the
STORED_MESSAGES setting.
For example your project's `settings.py` file might look like this::

    STORED_MESSAGES = {
        'INBOX_EXPIRE_DAYS': 30,
    }

This module provides the `stored_messages_settings` object, that is used to
access Stored Messages framework settings, checking for user settings first,
then falling back to the defaults.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.utils import six, importlib

from .constants import *

USER_SETTINGS = getattr(settings, 'STORED_MESSAGES', None)
MESSAGE_TAGS = getattr(settings, 'MESSAGE_TAGS', {})

DEFAULTS = {
    'STORE_LEVELS': (
        STORED_DEBUG,
        STORED_INFO,
        STORED_SUCCESS,
        STORED_WARNING,
        STORED_ERROR,
    ),
    'MESSAGE_TAGS': MESSAGE_TAGS.update({
        STORED_DEBUG: 'stored debug',
        STORED_INFO: 'stored info',
        STORED_SUCCESS: 'stored success',
        STORED_WARNING: 'stored warning',
        STORED_ERROR: 'stored error',
    }),
    'INBOX_EXPIRE_DAYS': 30,
    'STORAGE_BACKEND': 'stored_messages.backends.DefaultBackend',
    # Only for Redis backend
    'REDIS_URL': 'redis://username:password@localhost:6379/0',
}

# List of settings that cannot be empty
MANDATORY = (

)

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'STORAGE_BACKEND',
)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if isinstance(val, six.string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except ImportError as e:
        msg = "Could not import '%s' for setting '%s'. %s: %s." % (val, setting_name,
                                                                   e.__class__.__name__, e)
        raise ImportError(msg)


class StoredMessagesSettings(object):
    """
    A settings object, that allows settings to be accessed as properties.

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None, mandatory=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.import_strings = import_strings or ()
        self.mandatory = mandatory or ()

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid Stored Messages setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if val and attr in self.import_strings:
            val = perform_import(val, attr)

        self.validate_setting(attr, val)

        # Cache the result
        setattr(self, attr, val)
        return val

    def validate_setting(self, attr, val):
        if not val and attr in self.mandatory:
            raise AttributeError("Stored Messages setting: '%s' is mandatory" % attr)


stored_messages_settings = StoredMessagesSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS,
                                                  MANDATORY)
