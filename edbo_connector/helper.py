#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
EDBOWebApiHelper
Author: Eldar Aliiev
Email: e.aliiev@vnmu.edu.ua
"""

from __future__ import print_function
import sys
from edbo_connector.config import ECHO_ON


class EDBOWebApiHelper:
    """
    EDBOWebApiHelper - class which implements helper methods
    """

    @staticmethod
    def echo(message, color=None, force_exit=False):
        """Print information message to default output
        :param message: Information message
        :param color: Color of output (Default=None)
        :param force_exit: Color of output (Default=False)
        :type message: str
        :type color: str
        :type force_exit: bool
        """
        if ECHO_ON:
            if color is not None:  # Colored output
                color_code = {
                    'red': '0;31',
                    'green': '0;32',
                    'yellow': '1;33',
                    'cyan': '0;36',
                    'blue': '0;34',
                    'white': '1;37'
                }.get(color, '0')
                print('\033[%sm%s\033[0m' % (color_code, message))
            else:  # Simple output
                print(message)

            if force_exit:  # Need force exit from program
                sys.exit()

    @staticmethod
    def format_file_size(filesize, suffix='B'):
        """
        Humanize file size.
        :param filesize: Size of file in bytes
        :param suffix: Suffix which will be added to size format
        :return: Humanized file size
        """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(filesize) < 1024.0:
                return "%3.1f%s%s" % (filesize, unit, suffix)
            filesize /= 1024.0
