"""
The `compat` module provides support for backwards compatibility with older
versions of django and python..
"""

from __future__ import unicode_literals

import django
from django.conf import settings

# Django 1.5 add support for custom auth user model
if django.VERSION >= (1, 5):
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
else:
    AUTH_USER_MODEL = 'auth.User'

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User

# DRF 3.0 compatibility layer
try:
    from rest_framework.decorators import action as detail_route
except ImportError:
    from rest_framework.decorators import detail_route