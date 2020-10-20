import fourinsight.api

import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def response():
    response = Mock()
    return response


@pytest.fixture
def auth_session(response):
    auth_session = Mock()
    auth_session.get.return_value = response
    return auth_session


@pytest.fixture
def campaigns_api(auth_session):
    return fourinsight.api.api.CampaignsAPI(auth_session)


class Test_CampaignsAPI:

    def test_init(self, campaigns_api, auth_session):
        assert campaigns_api._auth_session == auth_session

    @patch("fourinsight.api.api.environment")
    def test_get_base_url(self, env_mock, campaigns_api):
        env_mock.api_base_url = "test"
        assert campaigns_api._get_base_url() == "test"

    def test__get(self, campaigns_api, response):
        assert campaigns_api._get("test") == response
        response.raise_for_status.assert_called_once()

    def test_verify_type(self, campaigns_api):
        assert campaigns_api._verify_type("SWIM Campaign") == "SWIM Campaign"
        assert campaigns_api._verify_type("Campaign") == "Campaign"

    def test_verify_type_raises(self, campaigns_api):
        with pytest.raises(ValueError):
            campaigns_api._verify_type("test")

    @patch("fourinsight.api.api.environment")
    def test_get_campaigns(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_campaigns()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_swim_campaigns(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api._get_swim_campaigns()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/SWIM Campaign")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_generic_campaigns(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api._get_generic_campaigns()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/Campaign")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_campaigns_swim(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_campaigns(campaign_type="SWIM Campaign")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/SWIM Campaign")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_campaigns_generic(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_campaigns(campaign_type="Campaign")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/Campaign")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_campaigns_raises(self, campaigns_api):
        with pytest.raises(ValueError):
            campaigns_api.get_campaigns(campaign_type="invalid_type")

    @patch("fourinsight.api.api.environment")
    def test_get_campaign(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_campaign("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_events(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_events("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/Events")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_sensors(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_sensors("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/Sensors")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_lowerstack(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_lowerstack("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/LowerStack")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_swimops_campaign(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_swimops_campaign("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/Swimops")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    @patch("fourinsight.api.api.environment")
    def test_get_swimops(self, env_mock, campaigns_api, auth_session, response):
        env_mock.api_base_url = "test"

        campaigns_api.get_swimops()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Swimops")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()
