EDBO-connector
==============

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