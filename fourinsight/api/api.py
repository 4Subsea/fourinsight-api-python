from fourinsight.api.globalsettings import environment


_CAMPAIGN_TYPES = [
    "SWIM Campaign",
    "Campaign",
]


class CampaignsAPI:
    """
    Python wrapper for api.4insight.io.

    Parameters
    ----------
    auth_session : subclass of ``requests.session``
        Authorized session instance which appends a valid bearer token to all
        HTTP calls.
    """

    def __init__(self, auth_session):
        self._auth_session = auth_session

    def _get_base_url(self):
        return environment.api_base_url

    def _get(self, *args, **kwargs):
        response = self._auth_session.get(*args, **kwargs)
        response.raise_for_status()
        return response

    def _verify_type(self, campaign_type):
        if campaign_type in _CAMPAIGN_TYPES:
            return campaign_type
        else:
            raise ValueError("Campaign type {campaign_type} not supported.")

    def _get_swim_campaigns(self):
        return self._get(
            self._get_base_url() + f"/v1.0/Campaigns/Type/SWIM Campaign"
        ).json()

    def _get_generic_campaigns(self):
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/Type/Campaign").json()

    def get_campaigns(self, campaign_type=None):
        """Campaign list.

        Parameters
        ----------
        campaign_type : str
            Campaign type ['Campaign', 'SWIM Campaign'].
        """
        if not campaign_type:
            return self._get(self._get_base_url() + "/v1.0/Campaigns").json()

        campaign_type = self._verify_type(campaign_type)
        if campaign_type == "SWIM Campaign":
            return self._get_swim_campaigns()
        elif campaign_type == "Campaign":
            return self._get_generic_campaigns()

    def get_campaign(self, campaign_id):
        """Campaign dict"""
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}").json()

    def get_events(self, campaign_id):
        """Events dict"""
        return self._get(
            self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/Events"
        ).json()

    def get_sensors(self, campaign_id):
        """Sensors dict"""
        return self._get(
            self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/Sensors"
        ).json()

    def get_lowerstack(self, campaign_id):
        """Lower Stack dict"""
        return self._get(
            self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/LowerStack"
        ).json()

    def get_swimops_campaign(self, campaign_id):
        """SWIM operations for campaign."""
        return self._get(
            self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/Swimops"
        ).json()

    def get_swimops(self):
        """SWIM operations list"""
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/Swimops").json()

    # def get_campaign_type(self, campaign_id):
    #     return self.get_campaign(campaign_id)["campaignType"]
