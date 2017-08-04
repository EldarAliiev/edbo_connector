EDBO-connector
==============

Python library for work with EDBO

https://github.com/ZimGreen/edbo-connector-py

Install:
--------

.. code-block:: bash

    $ git clone https://github.com/ZimGreen/edbo-connector-py.git
    $ cd edbo-connector-py
    $ python setup.py install

or with pip:

.. code-block:: bash

    $ pip install edbo_connector


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