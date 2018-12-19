# 导他妈的
from __future__ import unicode_literals
from collections import OrderedDict

try:
    from alienVan.appConfig import *

except ImportError:
    from alienVan.appConfig import *

# python2 兼容
# try:
#     from urlparse import urlparse # python 2
# except:
#     from urllib.parse import urlparse

import onedrivesdk
from onedrivesdk.helpers.resource_discovery import ResourceDiscoveryRequest
from os.path import splitext


# 初始化
# 非商业版(个人版)
def authenticate_init_N():
    '''
    用于普通版的oneDrive，office365商业版无法使用的初始化函数。
    用户登录，获取详细信息，将详细信息保存在conf文件中。
    在第一次登录时使用。
    :param client:
    :return:
    '''
    funcName = 'hentai'

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider = http_provider,
        client_id = client_id_normal,
        scopes = scopes)

    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    print(auth_url) # 登陆授权的URL
    code = input('Paste code here: ')
    client.auth_provider.authenticate(code, redirect_uri, client_secret_normal)
    # return client

    return auth_url,funcName

def init_business():
    '''
    备用
    用于登陆Business/Office 365版OneDrive的初始化函数。
    用户登录，获取详细信息，将详细信息保存在conf文件中。
    在第一次登录时使用。
    Ref:
    https://github.com/OneDrive/onedrive-sdk-python#onedrive-for-business
    https://dev.onedrive.com/auth/aad_oauth.htm#register-your-app-with-azure-active-directory
    :param client:
    :return:
    '''
    # auth url:
    # https://login.microsoftonline.com/common/oauth2/authorize?scope=wl.signin+wl.offline_access+onedrive.readwrite&redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=bac72a8b-77c8-4b76-8b8f-b7c65a239ce6

    funcName = 'business'

    http = onedrivesdk.HttpProvider()
    auth = onedrivesdk.AuthProvider(http,
                                    client_id_business,
                                    auth_server_url = auth_server_url,
                                    auth_token_url = auth_token_url)
    auth_url = auth.get_auth_url(redirect_uri)

    # now the url looks like "('https://login.microsoftonline.com/common/oauth2/authorize',)?redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=bac72a8b-77c8-4b76-8b8f-b7c65a239ce6"

    try:  # Python 2
        auth_url = auth_url.encode('utf-8').replace("('", '').replace("',)", '')
    except TypeError:
        auth_url = auth_url.replace("('", '').replace("',)", '')

    print(auth_url)

    code = input('Paste code here: ')

    auth.authenticate(code, redirect_uri, client_secret_business, resource = 'https://api.office.com/discovery/')

    # this step is slow
    service_info = ResourceDiscoveryRequest().get_service_info(auth.access_token)[0]

    auth.redeem_refresh_token(service_info.service_resource_id)

    client = onedrivesdk.OneDriveClient(service_info.service_resource_id + '_api/v2.0/', auth, http)


    return client,funcName

# 其他工具
def authUrlToClient(code,funcName):
    pass

if __name__ == '__main__':
    authenticate_init_N()