import os

from business_logic.facebook_api.facebook_constants import FacebookConstants
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi


def get_ads(fields, params):
    """
    Get `fields` of ads filtered by `params`

    :param fields: a list of fields to be queried
    :param params: a dict of conditions to filter ads
    :return: a list of qualified ad objects containing required `fields` if operation is successful
             None otherwise
    """
    FacebookAdsApi.init(access_token=FacebookConstants.access_token)

    try:
        res = AdAccount(FacebookConstants.account_id).get_ads(
            fields=fields,
            params=params
        )
    except Exception as e:
        print(e)
        return None

    return res


def create_ad(params):
    """
    Create an ad

    :param params: a dict containing parameters for the ad
    :return: an ad object containing id if operation is successful
             None otherwise
    """
    FacebookAdsApi.init(access_token=FacebookConstants.access_token)
    fields = []
    # ensure the ad set is initially paused
    params['status'] = 'PAUSED'

    try:
        res = AdAccount(FacebookConstants.account_id).create_ad(
            fields=fields,
            params=params,
        )
    except Exception as e:
        print(e)
        return None

    return res


def update_ad(ad_id, params):
    """
    Update an ad

    :param ad_id: a string or int representing the ad id
    :param params: a dict containing parameters and values to update
    :return: the exit status of the process if operation is successful
             -1 otherwise
    """
    FacebookAdsApi.init(access_token=FacebookConstants.access_token)
    cmd = "curl -X POST \\\n"
    for k, v in params.items():
        cmd += "    -F '{}={}' \\\n".format(k, v)
    cmd += "    -F 'access_token={}' \\\n".format(FacebookConstants.access_token)
    cmd += "    https://graph.facebook.com/v3.3/{}".format(ad_id)

    try:
        # TODO: use subprocess module instead of os.system
        res = os.system(cmd)
    except Exception as e:
        print(e)
        return -1

    return res


def delete_ad_by_id(ad_id):
    """
    Delete an ad by its id

    :param ad_id: a string or int representing the ad id
    :return: the exit status of the process if operation is successful
             -1 otherwise
    """
    cmd = """
        curl -X DELETE \
        -F 'access_token={}' \
        https://graph.facebook.com/v3.3/{}
    """.format(FacebookConstants.access_token, ad_id)

    try:
        # TODO: use subprocess module instead of os.system
        res = os.system(cmd)
    except Exception as e:
        print(e)
        return -1

    return res
