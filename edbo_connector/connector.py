#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
EDBOWebApiConnector
Author: Eldar Aliiev
Email: e.aliiev@vnmu.edu.ua
"""

import time
import requests
from requests.adapters import HTTPAdapter
import edbo_connector.config as config
from edbo_connector.helper import EDBOWebApiHelper


class EDBOWebApiConnector(object):
    """EDBOWebApiConnector - class which implements connection
    and method execution with EDBO RESTfull API.

    Attributes:
        url_prefix  Path to RESTful API server.
    """

    url_prefix = '%s/data/EDEBOWebApi' % config.EDBO_SERVER  # Build url to RESTful server

    def __init__(self, username=config.EDBO_USER, password=config.EDBO_PASSWORD):
        """Initialize connect and login into RESTful API server.
        :param username: Username (Default=from config file)
        :param password: Method data (Default=from config file)
        :type username: str
        :type password: str
        """
        self._status = None  # Initialize status
        self._execution_time = 0  # Initialize execution_time
        self._is_logged_in = False  # Is user logged in
        self._session = requests.Session()  # Initialize client session
        self._session.headers.update(self.default_headers)  # Set default headers to own
        self._session.mount(
            config.EDBO_SERVER,
            HTTPAdapter(max_retries=config.CONNECTION_RETRIES)
        )  # Mount RESTful API server to our session
        self.__login(username, password)  # Login into server

    def __del__(self):
        """End of session"""
        if self._is_logged_in:  # Check if user is logged in
            self.__logout()

    @property
    def status(self):
        """Return status of last request
        :return: Status of last method execution
        :rtype: int
        """
        return self._status

    @property
    def execution_time(self):
        """Return execution time of last request
        :return: Time of last method execution
        :rtype: float
        """
        return self._execution_time

    @property
    def default_headers(self):
        """Default request headers
        :return: Default request headers such as user-agent, referer and etc
        :rtype: dict
        """
        return {
            'Origin': config.EDBO_SERVER,
            'Referer': config.EDBO_SERVER,
            'User-Agent': config.USER_AGENT,
        }

    def __login(self, username=config.EDBO_USER, password=config.EDBO_PASSWORD):
        """Login request to RESTful API"""

        EDBOWebApiHelper.echo(u'Вхід в систему...')
        try:
            response = self._session.post(
                self.url_prefix + '/oauth/token',
                data={
                    'grant_type': 'password',
                    'username': username,
                    'password': password,
                    'app_key': config.EDBO_APPLICATION_KEY,
                },
                headers=self.default_headers
            )  # Send authorization request

            if response.status_code == 200:  # Check if authorization is successful
                self._session_start_time = time.time()  # Catch session start time
                self._status = response.status_code  # Catch last response status code
                self._is_logged_in = True  # Logged in
                self._session.headers.update({
                    'authorization': 'Bearer ' + response.json().get('access_token', None),
                })  # Add OAuth header
                EDBOWebApiHelper.echo(u'Вхід успішний, вітаю %s!' % config.EDBO_USER, color='green')
            elif response.status_code == 400:
                EDBOWebApiHelper.echo(
                    response.json().get('error', u'Трапилася невідома помилка!'),
                    color='red',
                    force_exit=True
                )  # Incorrect login data
            else:
                EDBOWebApiHelper.echo(
                    u'Не вдалося авторизуватися в системі!',
                    color='red',
                    force_exit=True
                )  # Fail if login is unsuccessful

        except requests.exceptions.ConnectionError:
            EDBOWebApiHelper.echo(
                u'Не вдалося встановити зв\'язок з сервером!',
                color='red',
                force_exit=True
            )

    def __logout(self):
        """Logout from server"""
        EDBOWebApiHelper.echo(u'Вихід з системи...', color='red')
        self.execute('auth/logout')  # Logout from server
        self._is_logged_in = False  # Logged out

    def execute(self, url, data=None, headers=None, json_format=True):
        """Send request to RESTful server.
        :param url: Path to RESTful method
        :param data: Method data (Default=empty)
        :param headers: Default headers (Default=empty)
        :param json_format: Return results dictionary or object (Default=True)
        :type url: str
        :type data: dict
        :type headers: dict
        :type json_format: bool
        :returns: Result of method execution
        :rtype: dict, object
        """
        if int(time.time() - self._session_start_time) > config.RELOGIN_AFTER:  # Check if session is not expired (15min)
            EDBOWebApiHelper.echo(u'Сесія добігає кінця, поновлення...')
            self.__logout()  # Logout from server
            self.__login()  # Login again

        time.sleep(config.EXECUTION_TIMEOUT)  # Wait between methods execution

        while True:  # Try to execute method
            try:
                EDBOWebApiHelper.echo(u'Виконання методу %s...' % url)
                execution_start = time.time()  # Catch start of execution
                response = self._session.post(
                    '%s/api/%s' % (self.url_prefix, url),
                    data if data is not None else {'': ''},
                    headers if headers is not None else {}
                )  # Send request to RESTful server
                execution_end = time.time()  # Catch end of execution
            except requests.exceptions.ConnectionError:  # Check if method execution is successful
                EDBOWebApiHelper.echo(
                    u'Виконання методу завершено невдало, повторна спроба...',
                    color='red'
                )
                continue  # Retry if unsuccessful
            break

        self._execution_time = execution_end - execution_start  # Save last execution time
        self._status = response.status_code  # Save last status code

        EDBOWebApiHelper.echo(
            u'Виконання методу завершено з кодом %d [%.3fs]' % (
                self._status,
                self._execution_time
            ),
            color='green'
        )

        if self._status == 200:  # Check if server return data
            return response.json() if json_format else response  # Return result of method execution
