Development using ``fourinsight.api``
=====================================

It may be helpful to redirect the API calls to a development backend during development.
This can be achieved by reconfiguring the API parameters on run-time::

    import fourinsight.api as fapi

    fapi.authenticate._CONSTANTS = {
        "API_BASE_URL": "https://api.4insight.io/",
        "USER_CLIENT_ID": "<Client ID used for UserSession>",
        "USER_CLIENT_SECRET": "<Client secret used for UserSession>",
        "USER_AUTHORITY_URL": "<Authority URL used for UserSession>",
        "CLIENT_TOKEN_URL": "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token",
        "CLIENT_SCOPE": ["https://4subseaid.onmicrosoft.com/4insight-api-prod/.default"]
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

* API_BASE_URL: "https://4insight-api-test.4subsea.net"
* USER_CLIENT_ID: "9176603a-f0e9-45ca-a615-15d8eb35d9d3"
* USER_CLIENT_SECRET: "vNIY8No17yF7gV.GN8mDou22gn.nZ_B.j3"
* USER_AUTHORITY_URL: "https://4insight-test.4subsea.net/auth"
* CLIENT_TOKEN_URL: "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
* CLIENT_SCOPE: ["https://4subseaid.onmicrosoft.com/4insight-api-test/.default"]

QA
--

* API_BASE_URL: "https://4insight-api-qa.4subsea.net"
* USER_CLIENT_ID: TBA
* USER_CLIENT_SECRET: TBA
* USER_AUTHORITY_URL: "https://4insight-qa.4subsea.net/auth"
* CLIENT_TOKEN_URL: "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
* CLIENT_SCOPE: ["https://4subseaid.onmicrosoft.com/4insight-qa-test/.default"]
