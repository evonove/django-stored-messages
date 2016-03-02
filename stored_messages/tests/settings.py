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

# Django 1.10 requires the TEMPLATES settings. Deprecated since Django 1.8
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SITE_ID = 1

MESSAGE_STORAGE = 'stored_messages.storage.PersistentStorage'
STORED_MESSAGES = {
    'REDIS_URL': 'redis://localhost:6379/0',
}

MOCK_REDIS_SERVER = False
SECRET_KEY = 'FUUUFU'
