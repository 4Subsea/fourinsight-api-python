import os
import json
from abc import ABCMeta, abstractmethod
from importlib.resources import read_text

from oauthlib.oauth2 import (
    WebApplicationClient,
    BackendApplicationClient,
    InvalidGrantError,
)
from requests_oauthlib import OAuth2Session

from .appdirs import user_data_dir


_CONSTANTS = json.loads(read_text("fourinsight.api", "_constants.json"))


class TokenCache:
    def __init__(self, session_key=None):
        self._session_key = session_key

        if not os.path.exists(self._token_root):
            os.makedirs(self._token_root)

        try:
            with open(self.token_path, "r") as f:
                self._token = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._token = {}

    def __call__(self, token):
        self.dump(token)

    def append(self, key, value):
        self._token[key] = value

    @property
    def _token_root(self):
        return user_data_dir("api")

    @property
    def token_path(self):
        if self._session_key is not None:
            return os.path.join(self._token_root, f"token.{self._session_key}")
        return os.path.join(self._token_root, "token")

    def dump(self, token):
        self._token.update(token)
        with open(self.token_path, "w") as f:
            json.dump(self._token, f)

    @property
    def token(self):
        return self._token or None


class BaseAuthSession(OAuth2Session, metaclass=ABCMeta):
    """
    Abstract class for authorized sessions.

    Parameters
    ----------
    client : ``oauthlib.oauth2`` client.
        A client passed on to ``requests_oauthlib.OAuth2Session``.
    token_url : str
        Token endpoint URL, must use HTTPS.
    session_params: dict
        Dictionary containing the necessary parameters used during
        authentication. Use these parameters when overriding the
        '_prepare_fetch_token_args' and '_prepare_refresh_token_args' methods.
        The provided dict is stored internally in '_session_params'.
    auth_force : bool, optional
        Force re-authenticating the session (default is False)
    kwargs : keyword arguments
        Keyword arguments passed on to ``requests_oauthlib.OAuth2Session``.
        Here, the mandatory parameters for the authentication client shall be
        provided.

    """

    def __init__(self, client, auth_force=False, **kwargs):
        super().__init__(
            client=client,
            **kwargs,
        )

        if auth_force or not self.token:
            token = self.fetch_token()
        else:
            try:
                token = self.refresh_token()
            except (KeyError, ValueError, InvalidGrantError):
                token = self.fetch_token()
            else:
                print("Authentication from previous session still valid.")

        if self.token_updater:
            self.token_updater(token)

    def fetch_token(self):
        """Fetch new access and refresh token."""
        args, kwargs = self._prepare_fetch_token_args()
        token = super().fetch_token(*args, **kwargs)
        return token

    def refresh_token(self, *args, **kwargs):
        """Refresh (expired) access token with a valid refresh token."""
        args, kwargs = self._prepare_refresh_token_args()
        token = super().refresh_token(*args, **kwargs)
        return token

    @abstractmethod
    def _prepare_fetch_token_args(self):
        """
        Prepare positional and keyword arguments passed on to
        ``OAuth2Session.fetch_token``. Subclass overrides.
        """
        args = ()
        kwargs = {}
        return args, kwargs

    @abstractmethod
    def _prepare_refresh_token_args(self):
        """
        Prepare positional and keyword arguments passed on to
        ``OAuth2Session.refresh_token``. Subclass overrides.
        """
        args = ()
        kwargs = {}
        return args, kwargs

    def get_rename_dict(self, url, key_map, **kwargs):
        response = super().get(url, **kwargs)
        response.raise_for_status()

        old_dict = response.json()
        new_dict = {}
        for old_key, new_key in key_map.items():
            new_dict[new_key] = old_dict[old_key]
        return new_dict


class UserSession(BaseAuthSession):
    """
    Authorized session where credentials are given in the 4insight.io web
    application. When a valid code is presented, the session is authenticated
    and persisted. A previous session will be reused as long as it is not
    expired. When required, a new authentication code is prompted for.

    Extends ``BaseAuthSession``.

    Parameters
    ----------
    auth_force : bool, optional
        Force re-authenticating the session (default is False)
    session_key : str, optional
        Unique identifier for an auth session. Can be used so that multiple
        instances can have independent auth/refresh cycles with the identity
        authority. Prevents local cache from being accidently overwritten.

    """

    def __init__(self, auth_force=False, session_key=None):
        self._api_base_url = _CONSTANTS["API_BASE_URL"]
        self._client_id = _CONSTANTS["USER_CLIENT_ID"]
        self._client_secret = _CONSTANTS["USER_CLIENT_SECRET"]
        self._authority_url = _CONSTANTS["USER_AUTHORITY_URL"]

        token_cache = TokenCache(session_key=session_key)
        token = token_cache.token

        if token:
            self._token_url = token.get("token_url", None)
        else:
            self._token_url = None

        client = WebApplicationClient(self._client_id)
        super().__init__(
            client,
            auth_force=auth_force,
            token_updater=token_cache,
            token=token,
            auto_refresh_url=self._token_url,
        )

    def _prepare_fetch_token_args(self):
        print(
            "Please go here and authorize,",
            self._authority_url,
        )
        package = input("Paste code here: ")
        parameters = json.loads(package)
        token_url = parameters["endpoint"]
        code = parameters["code"]

        self.token_updater.append("token_url", token_url)
        self._token_url = token_url
        self.auto_refresh_url = token_url

        args = (self._token_url,)
        kwargs = {
            "code": code,
            "client_secret": self._client_secret,
        }
        return args, kwargs

    def _prepare_refresh_token_args(self):
        args = (self._token_url,)
        kwargs = {
            "refresh_token": self.token["refresh_token"],
            "client_secret": self._client_secret,
        }
        return args, kwargs


class ClientSession(BaseAuthSession):
    """
    Authorized session where credentials are given as client_id and
    client_secret. When valid credentials are presented, the session is
    authenticated and persisted.

    Extends ``BaseAuthSession``.

    Parameters
    ----------
    client_id : str
        Unique identifier for the client (i.e. app/service etc.).
    client_secret : str
        Secret/password for the client.

    """

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_url = _CONSTANTS["CLIENT_TOKEN_URL"]
        self._scope = _CONSTANTS["CLIENT_SCOPE"]

        client = BackendApplicationClient(self._client_id)
        super().__init__(
            client,
            auth_force=True,
            auto_refresh_url=self._token_url,
            # unable to supress TokenUpdated expection without this dummy updater
            token_updater=lambda token: None,
        )

    def _prepare_fetch_token_args(self):
        args = (self._token_url, )
        kwargs = {
            "client_secret": self._client_secret,
            "scope": self._scope,
            "include_client_id": True,
        }
        return args, kwargs

    def _prepare_refresh_token_args(self):
        return

    def refresh_token(self, *args, **kwargs):
        """Refresh (expired) access token"""
        token = self.fetch_token()
        return token
