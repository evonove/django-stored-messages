# flake8: noqa
import django


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

# Django 1.8 has a new, minimal default set for MIDDLEWARE_CLASSES so be explicit
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

SITE_ID = 1

MESSAGE_STORAGE = 'stored_messages.storage.PersistentStorage'
STORED_MESSAGES = {
    'REDIS_URL': 'redis://localhost:6379/0',
}

MOCK_REDIS_SERVER = False
SECRET_KEY = 'FUUUFU'
