# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io

from setuptools import setup

def long_description():
    with io.open('README.rst', encoding='utf-8') as fp:
        return fp.read()

setup(
    name='django_inlines_actions',
    version=0.1,
    author='kvirtx@gmail.com',
    author_email='kvirtx@gmail.com',
    url='https://github.com/kvirt/django-inlines-actions',
    description='Actions for Django inline admin',
    long_description=long_description(),
    packages=[str('inlines_actions')],
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
