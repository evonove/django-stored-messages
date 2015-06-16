
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.sessions",
    "stored_messages",
]

try:
    import rest_framework
    INSTALLED_APPS.append("rest_framework")
except ImportError:
    pass


DEBUG = True
USE_TZ = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "stored_messages.sqlite",
    }
}

ROOT_URLCONF = "stored_messages.tests.urls"

# Django 1.7 has a new, minimal default set for MIDDLEWARE_CLASSES so be explicit
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SITE_ID = 1

MESSAGE_STORAGE = 'stored_messages.storage.PersistentStorage'
STORED_MESSAGES = {
    'REDIS_URL': 'redis://localhost:6379/0',
}

MOCK_REDIS_SERVER = False

import django

if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
    INSTALLED_APPS.append('discover_runner')
else:
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SECRET_KEY = 'FUUUFU'
