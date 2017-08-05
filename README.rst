EDBO-connector
==============

.. image:: https://img.shields.io/pypi/v/python-edbo-connector.svg
    :target: https://pypi.python.org/pypi/python-edbo-connector

.. image:: https://img.shields.io/pypi/l/python-edbo-connector.svg
    :target: https://raw.githubusercontent.com/EldarAliiev/python-edbo-connector/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/python-edbo-connector.svg
    :target: https://raw.githubusercontent.com/EldarAliiev/python-edbo-connector/master/LICENSE

.. image:: https://img.shields.io/pypi/status/python-edbo-connector.svg
    :target: https://pypi.python.org/pypi/python-edbo-connector

.. image:: https://img.shields.io/github/contributors/EldarAliiev/python-edbo-connector.svg
    :target: https://github.com/EldarAliiev/python-edbo-connector/graphs/contributors



Python library for work with EDBO

https://github.com/EldarAliiev/python-edbo-connector

Install:
--------

.. code-block:: bash

    $ git clone https://github.com/EldarAliiev/python-edbo-connector.git
    $ cd edbo-connector
    $ python setup.py install

or with pip:

.. code-block:: bash

    $ pip install python-edbo-connector

Usage example:
--------------

Before usage set some environment variables:

* EDBO_SERVER
* EDBO_USER
* EDBO_PASSWORD
* EDBO_APPLICATION_KEY

For example create **edbo_settings.py**:

.. code-block:: python

    import os

    os.environ['EDBO_SERVER'] = '192.168.180.22'
    os.environ['EDBO_USER'] = '<EDBO login>'
    os.environ['EDBO_PASSWORD'] = '**********'
    os.environ['EDBO_APPLICATION_KEY'] = '<Application key>'

And import it to your application:

.. code-block:: python

    import edbo_settings
    from edbo_connector import EDBOWebApiClient

    client = EDBOWebApiClient()
    result = client.get_specialities_list()
    print(result)

For disable debug output change **ECHO_ON** environment variable to *False*.
Full list of settings parameters you can find in **edbo_connector/config.py**.