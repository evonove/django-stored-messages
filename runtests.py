import sys
from optparse import OptionParser

try:
    from django.conf import settings

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

    import imp
    imp.find_module('django_nose')

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="stored_messages.urls",
        INSTALLED_APPS=INSTALLED_APPS,
        # Django 1.7 has a new, minimal default set for MIDDLEWARE_CLASSES so be explicit
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        MESSAGE_STORAGE='stored_messages.storage.PersistentStorage',
        STORED_MESSAGES={
            'REDIS_URL': 'redis://localhost:6379/0',
        },
        MOCK_REDIS_SERVER=True,
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
