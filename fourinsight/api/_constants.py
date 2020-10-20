# COMMON
ENV_DEV = "DEV"
ENV_TEST = "TEST"
ENV_QA = "QA"
ENV_PROD = "PROD"

API_BASE_URL_DEV = None
API_BASE_URL_TEST = "https://4insight-api-test.4subsea.net"
API_BASE_URL_QA = "https://4insight-api-qa.4subsea.net"
API_BASE_URL_PROD = "https://api.4insight.io"


# USER (B2C - NOT REALLY SECRETS...)
CLIENT_ID_DEV_USER = None
CLIENT_SECRET_DEV_USER = None
AUTHORITY_URL_DEV_USER = None


CLIENT_ID_TEST_USER = "9176603a-f0e9-45ca-a615-15d8eb35d9d3"
CLIENT_SECRET_TEST_USER = "vNIY8No17yF7gV.GN8mDou22gn.nZ_B.j3"
AUTHORITY_URL_TEST_USER = "https://fourinsight-api-test.azurewebsites.net/"


CLIENT_ID_QA_USER = "dabdd9b6-7167-4631-b074-1f28dbae55e5"   # not correct
CLIENT_SECRET_QA_USER = "Q7/5RU5%c;Q|vIfJl9r^Owb1"   # not correct
AUTHORITY_URL_QA_USER = "https://reservoir-api-qa.4subsea.net/account"


CLIENT_ID_PROD_USER = "6b879622-4c52-43a3-ba23-2e9595dd996b"   # not correct
CLIENT_SECRET_PROD_USER = "7gOrIf4b(8IH$13wea38$-x5"   # not correct
AUTHORITY_URL_PROD_USER = "https://reservoir-api.4subsea.net/account"   # not correct


# CLIENT
TOKEN_URL_DEV_CLIENT = None
SCOPE_DEV_CLIENT = None

TOKEN_URL_TEST_CLIENT = (
    "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
)
SCOPE_TEST_CLIENT = ["https://4subseaid.onmicrosoft.com/4insight-api-test/.default"]

TOKEN_URL_QA_CLIENT = (
    "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
)
SCOPE_QA_CLIENT = ["https://4subseaid.onmicrosoft.com/4insight-api-qa/.default"]

TOKEN_URL_PROD_CLIENT = (
    "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token"
)
SCOPE_PROD_CLIENT = ["https://4subseaid.onmicrosoft.com/4insight-api-prod/.default"]
