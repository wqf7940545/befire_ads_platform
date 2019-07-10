import os

from business_logic.facebook_api.facebook_constants import FacebookConstants
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi


def get_campaigns(fields, params):
    """
    Get `fields` of campaigns filtered by `params`

    :param fields: a list of fields to be queried
    :param params: a dict of conditions to filter campaigns
    :return: a list of qualified campaign objects containing required `fields` if operation is successful
             None otherwise
    """
    FacebookAdsApi.init(access_token=FacebookConstants.access_token)

    try:
        res = AdAccount(FacebookConstants.account_id).get_campaigns(
            fields=fields,
            params=params
        )
    except Exception as e:
        print(e)
        return None

    return res


def create_campaign(params):
    """
    Create a campaign

    :param params: a dict containing parameters for the campaign
    :return: a campaign object containing id if operation is successful
             None otherwise
    """
    FacebookAdsApi.init(access_token=FacebookConstants.access_token)
    fields = []
    # ensure the campaign is initially paused
    params['status'] = 'PAUSED'

    try:
        res = AdAccount(FacebookConstants.account_id).create_campaign(
            fields=fields,
            params=params
        )
    except Exception as e:
        print(e)
        return None

    return res


def update_campaign(campaign_id, params):
    """
    Update a campaign

    :param campaign_id: a string or int representing the campaign id
    :param params: a dict containing parameters and values to update
    :return: the exit status of the process if operation is successful
             -1 otherwise
    """
    FacebookAdsApi.init(access_token=FacebookConstants.access_token)
    cmd = "curl -X POST \\\n"
    for k, v in params.items():
        cmd += "    -F '{}={}' \\\n".format(k, v)
    cmd += "    -F 'access_token={}' \\\n".format(FacebookConstants.access_token)
    cmd += "    https://graph.facebook.com/v3.3/{}".format(campaign_id)

    try:
        # TODO: use subprocess module instead of os.system
        res = os.system(cmd)
    except Exception as e:
        print(e)
        return -1

    return res


def delete_campaign_by_id(campaign_id):
    """
    Delete a campaign by its id

    :param campaign_id: a string or int representing the campaign id
    :return: the exit status of the process if operation is successful
             -1 otherwise
    """
    cmd = """
        curl -X DELETE \
        -F 'access_token={}' \
        https://graph.facebook.com/v3.3/{}
    """.format(FacebookConstants.access_token, campaign_id)

    try:
        # TODO: use subprocess module instead of os.system
        res = os.system(cmd)
    except Exception as e:
        print(e)
        return -1

    return res


def delete_campaigns(delete_strategy, before_date=None, object_count=None):
    """
    Delete campaigns according to params
    NOTE: Not very useful for now; use `delete_campaign_by_id` instead

    :param delete_strategy: a string representing delete strategy
    :param before_date: a datetime, only delete campaigns before this date
    :param object_count: a int representing the object count
    :return: an object containing list of deleted ids and objects left to delete count if operation is successful
             None otherwise
    """
    FacebookAdsApi.init(access_token=FacebookConstants.access_token)
    fields = []
    params = {
        'before_date': before_date,
        'delete_strategy': delete_strategy,
        'object_count': object_count
    }

    try:
        res = AdAccount(FacebookConstants.account_id).delete_campaigns(
            fields=fields,
            params=params
        )
    except Exception as e:
        print(e)
        return None

    return res
