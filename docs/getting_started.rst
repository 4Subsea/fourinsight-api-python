Getting Started
===============

New to Python?
--------------
You need to have Python installed on your system before you can use this package.
Head over to `Python.org`_ for instructions.

Python version support
----------------------
Officially Python 3.11, 3.12, and 3.13. We aim to support the three most
recent major versions.

OS support
----------
This package is tested with the latest Windows, MacOS, and Ubuntu (Linux) versions.

Install
-------
``fourinsight.api`` can be installed via pip from `PyPI`_.

.. code-block:: shell

   pip install fourinsight-api

.. _upgrade:

Upgrade
-------
``fourinsight.api`` can be upgraded via pip from `PyPI`_.

.. code-block:: shell

   pip install --upgrade fourinsight-api

Authentication
--------------
Your data may be your most valued treasure and security is no laughing matter!
At least we take it very seriously. Every API call requires authentication and
every bit of data (pun intended) requires authorization to access.

Before you can start to use :py:mod:`fourinsight.api`, you need to be able to
authenticate. If your organization is granted access via federation,
then you may use your prefered method to authenticate as it is done within your
organization. For single user access, :ref:`contact us <support>` and we will hook you up.

For non-interactive applications (daemons), you would need
a set of ``client_id`` and ``client_secret``. :ref:`Contact us <support>` and we will help you.

.. _Python.org: https://python.org
.. _PyPI: https://pypi.org/
