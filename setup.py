#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from edbo_connector import (
    __name__ as package_name,
    __version__ as package_version,
    __license__ as package_license,
    __author__ as package_author,
    __email__ as package_author_email
)

setup(
    name=package_name,
    version=package_version,
    author=package_author,
    author_email=package_author_email,
    url='https://github.com/ZimGreen/edbo-connector-py',
    download_url='https://github.com/ZimGreen/edbo-connector-py/archive/master.zip',
    license=package_license,
    description='edbo_connector',
    long_description=open('README.rst').read(),
    packages=[
        'edbo_connector',
    ],
    install_requires=[
        'requests==2.18.3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable'
        'License :: OSI Approved :: %s License' % package_license,
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
    ],
    keywords=[
        'EDBO',
        'connector',
        'RESTful API',
        'EDBO client',
    ],
    zip_safe=False
)
