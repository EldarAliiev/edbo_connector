#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import run


def publish():
    """Publish package to PyPi repository"""
    run('python setup.py bdist_wheel sdist upload --sign')
