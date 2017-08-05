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


Before use rename **"config.example.py"** to **"config.py"** inside the package
and add your own configs.

Usage example:
--------------

.. code-block:: python

    from edbo_connector import EDBOWebApiClient

    client = EDBOWebApiClient()
    result = client.get_specialities_list()
    print(result)

For disable debug output change **ECHO_ON** variable to *False*.