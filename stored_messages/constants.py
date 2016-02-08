from django.contrib.messages.constants import *


STORED_DEBUG = DEBUG + 1
STORED_INFO = INFO + 1
STORED_SUCCESS = SUCCESS + 1
STORED_WARNING = WARNING + 1
STORED_ERROR = ERROR + 1

DEFAULT_TAGS.update({
    STORED_DEBUG: 'persisted debug',
    STORED_INFO: 'persisted info',
    STORED_SUCCESS: 'persisted success',
    STORED_WARNING: 'persisted warning',
    STORED_ERROR: 'persisted error',
})
