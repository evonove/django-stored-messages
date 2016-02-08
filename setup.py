# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import re

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('stored_messages')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-stored-messages',
    version=version,
    description='Django contrib.messages on steroids',
    long_description=readme + '\n\n' + history,
    author='evonove',
    author_email='info@evonove.it',
    url='https://github.com/evonove/django-stored-messages',
    packages=[
        'stored_messages',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.8',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-stored-messages',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
