# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os
import re

from setuptools import setup


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


setup(
    name='django-admin-inline-actions',
    version=0.1,
    author='kvirtx@gmail.com',
    author_email='kvirtx@gmail.com',
    url='https://github.com/kvirtx/django-admin-inline-actions',
    description='Actions for Django inline admin',
    long_description=read('README.rst'),
    packages=[str('admin_inline_actions')],
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords=[
        'django', 'admin', 'inline', 'actions', 'inline actions', 'django inline actions',
        'django admin', 'django admin inline actions',
    ],
)
