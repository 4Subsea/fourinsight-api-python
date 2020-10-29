Basic Usage
###########

The :py:mod:`fourinsight.api` library provides access to protected resources in
`4insight.io`_ through authenticated REST calls to `4insight REST APIs`_.

Authorization Code Flow
-----------------------

The steps below outline how to use the Authorization Code Grant Type workflow to
set up an authenticated session and get access to a protected resource in `4insight.io`_.

Set up an authenticated User Session::

    from fourinsight.api import UserSession

    user_session = UserSession()
    # Follow instructions to authenticated

Use the ``user_session.get`` method to get e.g. a list of available campaigns
in 4insight::

    response = user_session.get('https://api.4insight.io/v1.0/Campaigns')


Client Credentials Flow
-----------------------

The steps below outline how to use the Client Credentials Grant Type workflow to
set up an authenticated session and get access to a protected resource in `4insight.io`_.

Set up an authenticated Client Session using your ``client_id`` and ``client_secret``::

    from fourinsight.api import ClientSession

    client_session = ClientSession('client_id', 'client_secret')

Use the ``client_session.get`` method to get e.g. a list of available campaigns
in 4insight::

    response = client_session.get('https://api.4insight.io/v1.0/Campaigns')


.. _4insight.io: https://4insight.io
.. _4insight REST APIs: https://4insight.io/#/developer
