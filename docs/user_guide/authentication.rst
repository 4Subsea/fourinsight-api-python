Authentication and Authorization
================================

:py:mod:`fourinsight.api` supports two different approaches for making authenticated calls to the `4insight REST API`_ endpoints:

	* **Single user / interactive** (OAuth2 Authorization Code Grant Type workflow)
	* **Service account** / non-interactive client (OAuth2 Client Credentials Grant Type workflow)

Single User / Interactive
-------------------------
This is the preferred approach for single user interactive sessions, e.g. use in notebooks. The class for user authentication is :py:class:`UserSession`.
You will be guided to your organizations login webpage, and login as usual. (We will not see or store your credentials!).
Once authenticated, you can choose to re-use your (valid) access token (i.e. not be prompted to authenticate next time) or re-authenticate everytime:

.. code-block:: python

    from fourinsight.api import UserSession

    # Re-use (valid) access token from last sesssion 
    session = UserSession()

    # or re-authenticate
    session = UserSession(auth_force=True)

.. caution::

    Users on shared computers (with shared accounts) should always re-authenticate since access token
    from a different user may unintentionally be used.

If you desire to have multiple separate session, it is advisable to set a session key during authetication.
This will keep the sessions (token cache) separate:

.. code-block:: python

    session_0 = UserSession(session_key="my_unique_session_0")
    session_1 = UserSession(session_key="my_unique_session_1")

Access and refresh tokens recieved during authentication are stored persistently to disk:

    * Windows: ``%USERPROFILE\.fourinsight\api``
    * Linux: ``~/.fourinsight/api``
    * MacOs: ``~/.config/.fourinsight/api``

Service Account / Non-interactive Client
----------------------------------------
This is the recommended approach for applications / services making `4Insight REST API`_ calls, where
an authentication flow with user interaction is not feasible nor desired. The class for client authetication is :py:class:`ClientSession`.

Example:

.. code-block:: python

    from fourinsight.api import ClientSession

    session = ClientSession("my_client_id", "my_client_secret")

:ref:`Contact us <support>` to request *client id* and *client secret*.

.. Note::

    :py:class:`ClientSession` will always re-authenticate and not store access token persistently.


.. _4Insight.io: https://4insight.io
.. _4Insight REST API: https://4insight.io/#/developer
