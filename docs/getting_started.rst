
Getting Started
###############

Authentication and authorization
******************************************

Your data may be your most valued treasure and security is no laughing matter!
At least we take it very seriously. Every API call requires authentication and
every bit of data (pun intended) requires authorization to access.

Before you can start to use :py:mod:`fourinsight.api`, you need to be able to
authenticate. If your organization is granted access via federation,
then you may use your prefered method to authenticate as it is done within your
organization. For single user access, :ref:`contact us <support>` and we will hook you up.

For non-interactive applications (daemons), you would need
a set of ``client_id`` and ``client_secret``. :ref:`Contact us <support>` and we will help you.

How to install
**************

:py:mod:`fourinsight.api` is written in pure Python and supports Windows,
Linux, and MacOS. Python >=3.7 is officially supported.

.. _install-upgrade:

To install using `pip`_::

   pip install fourinsight-api

And to upgrade to the latest version::

   pip install --upgrade fourinsight-api


.. _pip: https://pypi.org/project/fourinsight-api/
