Development using ``fourinsight.api``
=====================================

It may be helpful to redirect the API calls to development backend. This can be
achieved by reconfiguring the API parameters on run-time::

    import fourinsight.api as fapi

    fapi.authenticate._CONSTANTS = {
        "API_BASE_URL": "<URL for REST API endpoint>",
        "USER_CLIENT_ID": "<Client ID used for UserSession>",
        "USER_CLIENT_SECRET": "<Client secret used for UserSession>",
        "USER_AUTHORITY_URL": "<Authority URL used for UserSession>",
        "CLIENT_TOKEN_URL": "<Token URL used for ClientSession>",
        "CLIENT_SCOPE": ["<List of scopes used for ClientSession>"]
    }

    session = fapi.UserSession()

The parameters for different development environments are listed below:

Local development
-----------------

* API_BASE_URL: TBA
* USER_CLIENT_ID: TBA
* USER_CLIENT_SECRET: TBA
* USER_AUTHORITY_URL: TBA
* CLIENT_TOKEN_URL: TBA
* CLIENT_SCOPE: [TBA]

Test
----

* API_BASE_URL: TBA
* USER_CLIENT_ID: TBA
* USER_CLIENT_SECRET: TBA
* USER_AUTHORITY_URL: TBA
* CLIENT_TOKEN_URL: TBA
* CLIENT_SCOPE: [TBA]

QA
--

* API_BASE_URL: TBA
* USER_CLIENT_ID: TBA
* USER_CLIENT_SECRET: TBA
* USER_AUTHORITY_URL: TBA
* CLIENT_TOKEN_URL: TBA
* CLIENT_SCOPE: [TBA]