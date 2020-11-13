Development using ``fourinsight.api``
=====================================

It may be helpful to redirect the API calls to a development backend during development.
This can be achieved by reconfiguring the API parameters on run-time::

    import fourinsight.api as fapi

    fapi.authenticate._CONSTANTS = {
        "API_BASE_URL": "https://api.4insight.io/",
        "USER_CLIENT_ID": "b6c8c4d4-5fc1-4bba-b46c-8f6a6cc9843d",
        "USER_CLIENT_SECRET": "H_McZ-g.56~SS1d4SxCcSUTp~0Sv3AVERk",
        "USER_AUTHORITY_URL": "https://4insight.io/auth",
        "CLIENT_TOKEN_URL": "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token",
        "CLIENT_SCOPE": ["https://4subseaid.onmicrosoft.com/4insight-api-prod/.default"]
    }

    session = fapi.UserSession()

The parameters for different development environments are listed below:

Local development
-----------------

* API_BASE_URL: "https://localhost:44316"
* USER_CLIENT_ID: "b6c8c4d4-5fc1-4bba-b46c-8f6a6cc9843d"
* USER_CLIENT_SECRET: "H_McZ-g.56~SS1d4SxCcSUTp~0Sv3AVERk"
* USER_AUTHORITY_URL: "https://localhost:44316/auth"
* CLIENT_TOKEN_URL: "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
* CLIENT_SCOPE: ["https://4subseaid.onmicrosoft.com/4insight-api-dev/.default"]

Test
----

* API_BASE_URL: "https://4insight-api-test.4subsea.net"
* USER_CLIENT_ID: "b6c8c4d4-5fc1-4bba-b46c-8f6a6cc9843d"
* USER_CLIENT_SECRET: "H_McZ-g.56~SS1d4SxCcSUTp~0Sv3AVERk"
* USER_AUTHORITY_URL: "https://4insight-test.4subsea.net/auth"
* CLIENT_TOKEN_URL: "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
* CLIENT_SCOPE: ["https://4subseaid.onmicrosoft.com/4insight-api-test/.default"]

QA
--

* API_BASE_URL: "https://4insight-api-qa.4subsea.net"
* USER_CLIENT_ID: "b6c8c4d4-5fc1-4bba-b46c-8f6a6cc9843d"
* USER_CLIENT_SECRET: "H_McZ-g.56~SS1d4SxCcSUTp~0Sv3AVERk"
* USER_AUTHORITY_URL: "https://4insight-qa.4subsea.net/auth"
* CLIENT_TOKEN_URL: "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
* CLIENT_SCOPE: ["https://4subseaid.onmicrosoft.com/4insight-qa-test/.default"]
