import inspect
import json
import logging
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

import fourinsight.api as fapi
from fourinsight.api import authenticate

_CONSTANTS = authenticate._CONSTANTS


def test_constants():
    constants_out = authenticate._CONSTANTS

    constants_expected = {
        "API_BASE_URL": "https://api.4insight.io/",
        "USER_CLIENT_ID": "b6c8c4d4-5fc1-4bba-b46c-8f6a6cc9843d",
        "USER_CLIENT_SECRET": "H_McZ-g.56~SS1d4SxCcSUTp~0Sv3AVERk",
        "USER_AUTHORITY_URL": "https://4insight.io/auth",
        "CLIENT_TOKEN_URL": "https://login.microsoftonline.com/4subseaid.onmicrosoft.com/oauth2/v2.0/token",
        "CLIENT_SCOPE": [
            "https://4subseaid.onmicrosoft.com/4insight-api-prod/.default"
        ],
    }
    assert constants_out == constants_expected


@patch("fourinsight.api.authenticate.user_data_dir")
class Test_TokenCache:
    def test_init_dir_doesnt_exists(self, mock_cache_dir, tmp_path):

        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir

        assert not cache_dir.exists()
        authenticate.TokenCache()
        assert cache_dir.exists()

    def test_init_dir_exists(self, mock_cache_dir, tmp_path):
        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir
        cache_dir.mkdir()

        assert cache_dir.exists()
        token_cache = authenticate.TokenCache()

        assert token_cache._token == {}

    def test_init_cache_exists(self, mock_cache_dir, tmp_path):
        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir
        cache_dir.mkdir()

        cache_path = cache_dir / "token"

        with open(cache_path, "w") as f:
            json.dump({"access_token": "123abc"}, f)

        token_cache = authenticate.TokenCache()
        assert token_cache._token == {"access_token": "123abc"}

    def test__token_root(self, mock_cache_dir, tmp_path):
        my_dir = tmp_path / "my_dir"
        mock_cache_dir.return_value = my_dir

        token_cache = authenticate.TokenCache()
        token_root = token_cache._token_root

        assert token_root == my_dir

        mock_cache_dir.assert_called_with("api")

    def test_token_path(self, mock_cache_dir, tmp_path):
        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir

        cache_path = cache_dir / "token"

        token_cache = authenticate.TokenCache()
        assert token_cache.token_path == str(cache_path)

    def test_token_path_session_key(self, mock_cache_dir, tmp_path):
        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir

        session_key = "my_session_key"
        cache_path = cache_dir / f"token.{session_key}"

        token_cache = authenticate.TokenCache(session_key=session_key)
        assert token_cache.token_path == str(cache_path)

    def test_token(self, mock_cache_dir, tmp_path):
        my_dir = tmp_path / "my_dir"
        mock_cache_dir.return_value = my_dir

        token_cache = authenticate.TokenCache()
        token_cache._token = {"access_token": "123abc"}

        assert token_cache.token == {"access_token": "123abc"}

    def test_token_none(self, mock_cache_dir, tmp_path):
        my_dir = tmp_path / "my_dir"
        mock_cache_dir.return_value = my_dir

        token_cache = authenticate.TokenCache()

        assert token_cache.token is None

    def test_append(self, mock_cache_dir, tmp_path):
        my_dir = tmp_path / "my_dir"
        mock_cache_dir.return_value = my_dir

        token_cache = authenticate.TokenCache()
        token_cache._token = {"access_token": "123abc"}

        token_cache.append("new_key", "new_value")

        assert token_cache.token == {"access_token": "123abc", "new_key": "new_value"}

    def test_dump_session_key(self, mock_cache_dir, tmp_path):
        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir

        session_key = "my_session_key"
        cache_path = cache_dir / f"token.{session_key}"

        token_cache = authenticate.TokenCache(session_key=session_key)

        token = {"access_token": "123abc"}
        token_cache.dump(token)

        with open(cache_path, "r") as f:
            token_output = json.load(f)

        assert token == token_output

    def test_dump(self, mock_cache_dir, tmp_path):
        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir
        cache_dir.mkdir()

        cache_path = cache_dir / "token"

        token_cache = authenticate.TokenCache()

        token = {"access_token": "123abc"}
        token_cache.dump(token)

        with open(cache_path, "r") as f:
            token_output = json.load(f)

        assert token == token_output

    def test_dump_append(self, mock_cache_dir, tmp_path):
        cache_dir = tmp_path / "cache_dir"
        mock_cache_dir.return_value = cache_dir
        cache_dir.mkdir()

        cache_path = cache_dir / f"token"

        token_cache = authenticate.TokenCache()
        token_cache.append("new_key", "new_value")

        token = {"access_token": "123abc"}
        token_cache.dump(token)

        with open(cache_path, "r") as f:
            token_output = json.load(f)

        token.update({"new_key": "new_value"})
        assert token == token_output

    def test_call(self, mock_cache_dir, tmp_path):
        my_dir = tmp_path / "my_dir"
        mock_cache_dir.return_value = my_dir
        token_cache = authenticate.TokenCache()

        with patch.object(token_cache, "dump") as mock_dump:
            token_cache({"access_token": "123abc"})

        mock_dump.assert_called_once_with({"access_token": "123abc"})


@patch("fourinsight.api.authenticate.OAuth2Session.refresh_token")
@patch("fourinsight.api.authenticate.OAuth2Session.fetch_token")
class Test_ClientSession:
    def test_init(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        mock_fetch.assert_called_once_with(
            _CONSTANTS["CLIENT_TOKEN_URL"],
            client_secret="my_client_secret",
            scope=_CONSTANTS["CLIENT_SCOPE"],
            include_client_id=True,
        )
        assert auth.auto_refresh_url == _CONSTANTS["CLIENT_TOKEN_URL"]
        assert (
            auth.headers["user-agent"] == f"python-fourinsight-api/{fapi.__version__}"
        )

    def test_refresh_token(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")
        auth.refresh_token()
        mock_fetch.assert_called()

    def test_prepare_refresh_token_args(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        assert auth._prepare_refresh_token_args() is None

    def test_prepare_fetch_token_args(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        args, kwargs = auth._prepare_fetch_token_args()

        args_expected = (_CONSTANTS["CLIENT_TOKEN_URL"],)
        kwargs_expected = {
            "client_secret": "my_client_secret",
            "scope": _CONSTANTS["CLIENT_SCOPE"],
            "include_client_id": True,
        }

        assert args == args_expected
        assert kwargs == kwargs_expected

    def test_fetch_token(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        auth.fetch_token()

        mock_fetch.assert_called_with(
            _CONSTANTS["CLIENT_TOKEN_URL"],
            client_secret="my_client_secret",
            scope=_CONSTANTS["CLIENT_SCOPE"],
            include_client_id=True,
        )


@patch("fourinsight.api.authenticate.OAuth2Session.refresh_token")
@patch("fourinsight.api.authenticate.OAuth2Session.fetch_token")
@patch("fourinsight.api.authenticate.TokenCache")
class Test_UserSession:
    def test_init_force_auth(self, mock_token, mock_fetch, mock_refresh):
        with patch.object(
            authenticate.UserSession, "_prepare_fetch_token_args"
        ) as mock_fetch_args:
            mock_fetch_args.return_value = (
                ("my_token_url",),
                {
                    "code": "my_code",
                    "client_secret": _CONSTANTS["USER_CLIENT_SECRET"],
                },
            )

            auth = authenticate.UserSession(auth_force=True)

            assert (
                auth.headers["user-agent"]
                == f"python-fourinsight-api/{fapi.__version__}"
            )

            mock_fetch.assert_called_once_with(
                "my_token_url",
                code="my_code",
                client_secret=_CONSTANTS["USER_CLIENT_SECRET"],
            )
        mock_token.assert_called()
        auth.token_updater.assert_called()

    def test_init_session_key(self, mock_token, mock_fetch, mock_refresh):
        with patch.object(
            authenticate.UserSession, "_prepare_fetch_token_args"
        ) as mock_fetch_args:
            mock_fetch_args.return_value = (
                ("my_token_url",),
                {
                    "code": "my_code",
                    "client_secret": _CONSTANTS["USER_CLIENT_SECRET"],
                },
            )

            authenticate.UserSession(auth_force=True, session_key="test")
            mock_token.assert_called_once_with(session_key="test")

    def test_init_force_auth_false_token_none(
        self, mock_token, mock_fetch, mock_refresh
    ):
        with patch.object(
            authenticate.UserSession, "_prepare_fetch_token_args"
        ) as mock_fetch_args:
            mock_fetch_args.return_value = (
                ("my_token_url",),
                {
                    "code": "my_code",
                    "client_secret": _CONSTANTS["USER_CLIENT_SECRET"],
                },
            )

            token_cache = MagicMock()
            token_cache.token = None
            mock_token.return_value = token_cache

            authenticate.UserSession(auth_force=False)

            mock_fetch.assert_called_once_with(
                "my_token_url",
                code="my_code",
                client_secret=_CONSTANTS["USER_CLIENT_SECRET"],
            )

    def test_init_force_auth_false_token_valid(
        self, mock_token, mock_fetch, mock_refresh
    ):
        token_cache = MagicMock()
        token_cache.token = {
            "access_token": "my_access_token",
            "refresh_token": "my_refresh_token",
            "token_url": "my_token_url",
        }
        mock_token.return_value = token_cache

        auth = authenticate.UserSession(auth_force=False)

        mock_refresh.assert_called_once_with(
            "my_token_url",
            refresh_token="my_refresh_token",
            client_secret=_CONSTANTS["USER_CLIENT_SECRET"],
        )

        assert auth.token == token_cache.token
        assert auth.auto_refresh_url == "my_token_url"

    def test__prepare_refresh_token_args(self, mock_token, mock_fetch, mock_refresh):
        """Assume valid token in cache"""
        token_cache = MagicMock()
        token_cache.token = {
            "access_token": "my_access_token",
            "refresh_token": "my_refresh_token",
            "token_url": "my_token_url",
        }
        mock_token.return_value = token_cache

        auth = authenticate.UserSession(auth_force=False)

        args, kwargs = auth._prepare_refresh_token_args()
        assert args == ("my_token_url",)
        assert kwargs == {
            "refresh_token": "my_refresh_token",
            "client_secret": _CONSTANTS["USER_CLIENT_SECRET"],
        }

    def test_refesh_token(self, mock_token, mock_fetch, mock_refresh):
        """Assume valid token in cache"""
        token_cache = MagicMock()
        token_cache.token = {
            "access_token": "my_access_token",
            "refresh_token": "my_refresh_token",
            "token_url": "my_token_url",
        }
        mock_token.return_value = token_cache

        auth = authenticate.UserSession(auth_force=False)
        auth.refresh_token()

        mock_refresh.assert_called_with(
            "my_token_url",
            refresh_token="my_refresh_token",
            client_secret=_CONSTANTS["USER_CLIENT_SECRET"],
        )
        assert mock_refresh.call_count == 2

    def test_fetch_token(self, mock_token, mock_fetch, mock_refresh):
        with patch.object(
            authenticate.UserSession, "_prepare_fetch_token_args"
        ) as mock_fetch_args:
            mock_fetch_args.return_value = (
                ("my_token_url",),
                {
                    "code": "my_code",
                    "client_secret": _CONSTANTS["USER_CLIENT_SECRET"],
                },
            )

            auth = authenticate.UserSession(auth_force=True)
            auth.fetch_token()

        mock_fetch.assert_called_with(
            "my_token_url",
            code="my_code",
            client_secret=_CONSTANTS["USER_CLIENT_SECRET"],
        )
        assert mock_fetch.call_count == 2

    @patch("fourinsight.api.authenticate.input")
    def test_prepare_fetch_token_args(
        self, mock_input, mock_token, mock_fetch, mock_refresh
    ):
        token_cache = MagicMock()
        token_cache.token = None
        mock_token.return_value = token_cache

        mock_input.return_value = (
            '{"endpoint":"https://token-endpoint.com","code":"abc321"}'
        )

        auth = authenticate.UserSession(auth_force=True)
        args, kwargs = auth._prepare_fetch_token_args()

        assert args == ("https://token-endpoint.com",)
        assert kwargs == {
            "code": "abc321",
            "client_secret": _CONSTANTS["USER_CLIENT_SECRET"],
        }


@patch("fourinsight.api.authenticate.OAuth2Session.refresh_token")
@patch("fourinsight.api.authenticate.OAuth2Session.fetch_token")
class Test_BaseAuthSession:
    """
    Using ClientSession to initiate, but will only test methods and behavior
    provided by BaseAuthSession.
    """

    def test_update_args_kwargs_error(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        args = ()
        kwargs = {"something": 1}

        with pytest.raises(KeyError):
            auth._update_args_kwargs(args, kwargs)

    def test_update_args_kwargs_args_none(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        args = ()
        kwargs = {"method": "GET", "url": "/v1.0/ding/dong", "other": "thing"}

        args_out, kwargs_out = auth._update_args_kwargs(args, kwargs)

        assert (
            args
            + (
                "GET",
                auth._api_base_url + "/v1.0/ding/dong",
            )
            == args_out
        )
        assert {"timeout": auth._defaults["timeout"], "other": "thing"} == kwargs_out

    def test_update_args_kwargs_args_len_1(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        args = ("get",)
        kwargs = {"url": "/v1.0/ding/dong", "other": "thing"}

        args_out, kwargs_out = auth._update_args_kwargs(args, kwargs)

        assert args + (auth._api_base_url + "/v1.0/ding/dong",) == args_out
        assert {"timeout": auth._defaults["timeout"], "other": "thing"} == kwargs_out

    def test_update_args_kwargs_args(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        args = ("get", "/v1.0/ding/dong")
        kwargs = {"other": "thing"}

        args_out, kwargs_out = auth._update_args_kwargs(args, kwargs)

        assert args[:1] + (auth._api_base_url + "/v1.0/ding/dong",) == args_out
        assert {"timeout": auth._defaults["timeout"], "other": "thing"} == kwargs_out

    def test_update_args_kwargs_args_long(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")

        args = ("get", "/v1.0/ding/dong", "something")
        kwargs = {"other": "thing"}

        args_out, kwargs_out = auth._update_args_kwargs(args, kwargs)

        assert (
            args[:1] + (auth._api_base_url + "/v1.0/ding/dong",) + args[2:] == args_out
        )
        assert {"timeout": auth._defaults["timeout"], "other": "thing"} == kwargs_out

    @patch("fourinsight.api.authenticate.OAuth2Session.request")
    def test_request_relative_path(self, mock_request, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")
        args = ("/v1.0/ding/dong",)

        auth.get(*args)

        mock_request.assert_called_with(
            "GET", auth._api_base_url + args[0], allow_redirects=True, **auth._defaults
        )

    @patch("fourinsight.api.authenticate.OAuth2Session.request")
    def test_request_abs_path(self, mock_request, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")
        args = ("https://v1.0/ding/dong",)

        auth.get(*args)

        mock_request.assert_called_with(
            "GET", args[0], allow_redirects=True, **auth._defaults
        )

    @patch("fourinsight.api.authenticate.OAuth2Session.request")
    def test_request_logger(self, mock_request, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")
        args = ("https://v1.0/ding/dong",)

        log = logging.getLogger("fourinsight.api")
        log.setLevel("DEBUG")
        stream = StringIO()

        log.addHandler(logging.StreamHandler(stream))

        auth.get(*args)
        stream.seek(0)
        log_out = stream.read()
        assert log_out.startswith("request initiated")

    def test_get_pages_call_get(self, mock_fetch, mock_refresh):
        with patch.object(authenticate.ClientSession, "get") as mock_get:

            test_url = "myurl"
            gen = authenticate.ClientSession(
                "my_client_id", "my_client_secret"
            ).get_pages(test_url)
            next(gen)

            mock_get.assert_called_once_with(test_url)

    def test_get_pages_call_get_with_kwargs(self, mock_fetch, mock_refresh):
        with patch.object(authenticate.ClientSession, "get") as mock_get:

            test_url = "myurl"
            gen = authenticate.ClientSession(
                "my_client_id", "my_client_secret"
            ).get_pages(test_url, b="True")
            next(gen)

            mock_get.assert_called_once_with(test_url, b="True")

    def test_get_pages_response_object(self, mock_fetch, mock_refresh):
        auth = authenticate.ClientSession("my_client_id", "my_client_secret")
        gen = auth.get_pages("myurl")
        assert inspect.isgenerator(gen)


if __name__ == "__main__":
    pytest.main()
