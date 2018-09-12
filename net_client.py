from urllib.parse import *
from argparse import ArgumentParser
import requests
import re
from common_utils_py.helpers import *
from common_utils_py.logger_router import LoggerRouter
import os

logger = LoggerRouter().getLogger(__name__)


class NetClient(object):
    _COOKIE_TEMPLATE = {
        'EPORTAL_COOKIE_DOMAIN': '',
        'EPORTAL_COOKIE_SAVEPASSWORD': 'true',
        'EPORTAL_COOKIE_USERNAME': None,
        'EPORTAL_COOKIE_PASSWORD': None,
        'EPORTAL_COOKIE_SERVER': '',
        'EPORTAL_COOKIE_SERVER_NAME': quote('请选择服务'),
        'EPORTAL_COOKIE_OPERATORPWD': '',
        'EPORTAL_AUTO_LAND': '',
        'EPORTAL_USER_GROUP': quote('本科生'),
        'JSESSIONID': '0B3F329ED7FB4D8B5810D95F1973595D'
    }

    _POST_TEMPLATE = {
        'userId': None,
        'password': None,
        'service': '',
        'queryString': None,
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': ''
    }

    HEALTH_CHECK_URL = 'http://baidu.com'

    UNHEALTH_PATTERN = re.compile(r"top\.self\.location\.href='(.*)'")

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = self.COOKIE_TEMPLATE
        self.post_params = self.POST_TEMPLATE
        self.cookies['EPORTAL_COOKIE_USERNAME'] = self.username
        self.cookies['EPORTAL_COOKIE_PASSWORD'] = self.password
        self.post_params['userId'] = self.username
        self.post_params['password'] = self.password
        self._update_redir_url()

    @property
    def COOKIE_TEMPLATE(self):
        return NetClient._COOKIE_TEMPLATE.copy()

    @property
    def POST_TEMPLATE(self):
        return NetClient._POST_TEMPLATE.copy()

    def login(self):
        do_with_retry(10, 'Login failed', logger, self._login)

    def logout(self):
        do_with_retry(10, 'Logout failed', logger, self._logout)

    def _login(self):
        health_check_resp = requests.get(self.HEALTH_CHECK_URL)
        health_check_body = health_check_resp.text

        logger.info('Health check body:\n{}'.format(health_check_body))

        # print(health_check_resp.status_code)
        # print(health_check_resp.history)
        # print(health_check_resp.headers)
        # print(health_check_resp.text)

        redir_url_found = self.UNHEALTH_PATTERN.findall(health_check_body)
        if len(redir_url_found) == 1:
            logger.info('Now we are unhealthy, trying to reconnect...')
            redir_url = redir_url_found[0]
            logger.info('Fetched new redir_url: {}'.format(redir_url))
            self._update_redir_url(redir_url)
            return self._action('login')
        else:
            logger.info('No new redir_url found, maybe we are healthy')
            return

        # print('fuck')

    def _logout(self):
        self._action('logout')

    def _update_redir_url(self, url=None):
        if url is None:
            if os.path.isfile('last_url'):
                with open('last_url', 'r') as f:
                    self.redir_url = f.readline()
                logger.info('Use last redir_url')
            else:
                self.redir_url = None
                logger.warning('Cannot read last_url, maybe updated later')
        else:
            with open('last_url', 'w') as f:
                f.write(url)
                logger.info('Saved new redir_url')
            self.redir_url = url
        logger.info('Currently used redir_url: {}'.format(self.redir_url))
        redir_parse = urlparse(self.redir_url)
        self.gateway = '{}://{}/eportal/InterFace.do'.format(redir_parse.scheme, redir_parse.netloc)
        self.post_params['queryString'] = quote(redir_parse.query)

    def _action(self, method):
        get_param = {
            'method': method
        }
        resp = requests.post(self.gateway, data=self.post_params, params=get_param, cookies=self.cookies)

        resp_json = resp.json()

        success = resp_json['result'] == 'success'

        if success:
            logger.info('Action {} success, response = {}'.format(method, resp_json))
        else:
            logger.error('Action {} failed, response = {}'.format(method, resp_json))

        return success
