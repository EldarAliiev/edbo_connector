#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
EDBOWebApiClient
Author: Eldar Aliiev
Email: e.aliiev@vnmu.edu.ua
"""

import re
import edbo_connector.config as config
from edbo_connector.connector import EDBOWebApiConnector
from edbo_connector.helper import EDBOWebApiHelper
from edbo_connector.methods import EDBOWebApiMethods


class EDBOWebApiClient(EDBOWebApiMethods):
    """EDBOWebApiClient - class which implements some RESTful API methods
    and interface for methods execution by their names.
    """

    def __init__(self, username=config.EDBO_USER, password=config.EDBO_PASSWORD):
        """Initialize connector and prepare client to work
        :param username: Username (Default=from config file)
        :param password: Method data (Default=from config file)
        :type username: str
        :type password: str
        """
        self._connector = EDBOWebApiConnector(username, password)  # Initialize connector
        self._university_info = self._connector.execute('university/list')[0]  # Get university info

    def __getattr__(self, method):
        """Call RESTful API method
        :param method: Method of RESTful API
        :type method: str
        :return: Method for execution
        :rtype: function
        """

        if re.match(r'([0-9a-z_]+)', method) is not None:  # Check if method name is valid
            url = method.replace('_', '/')  # Transform method name into url

            def wrapper(data=None, headers=None, json_format=True):
                return self._connector.execute(
                    url,
                    data,
                    headers,
                    json_format
                )  # Send request to server

            return wrapper
        else:  # Fail if method is incorrect
            EDBOWebApiHelper.echo(u'Некоректний метод!', color='red')
            return

    def get_status(self):
        """Return status of last request
        :return: Status of last method execution
        :rtype: int
        """
        return self._connector.status

    def get_execution_time(self):
        """Return execution time of last request
        :return: Time of last method execution
        :rtype: float"""
        return self._connector.execution_time

    def get_user_info(self):
        """Get information about current user
        :return: Information about current user
        :rtype: dict
        """
        return self._connector.execute('auth/userInfo')

    def get_university_info(self, field):
        """Get university info
        :param field: Name of field
        :type field: str
        :return: University info field
        :rtype: str, int
        """
        return self._university_info.get(field, None)
