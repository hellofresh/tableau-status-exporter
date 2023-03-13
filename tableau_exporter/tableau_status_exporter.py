import json
import os
import requests
import logging
import datetime
from prometheus_client import generate_latest, REGISTRY
from server_parser_status_metrics import TableauServerStatusParser
from prometheus_client.twisted import MetricsResource
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class TokenManager(object):
    def __init__(self, user, password, site, host, api_version, token_name=None, token_secret=None):
        self._token = None
        self._api_version = api_version
        self.host = host

        if user and token_name:
            raise ValueError('Either a user/password OR token name/secret should be provided, not both.')
        elif user and password:
            self._creds = {
                'name': user,
                'password': password,
            }
        elif token_name and token_secret:
            self._creds = {
                'personalAccessTokenName': token_name,
                'personalAccessTokenSecret': token_secret,
            }
        else:
            raise ValueError('Either a user/password OR token name/secret must be provided.')

        self._creds['site'] = {'contentUrl': site}

    def _setup(self):
        body = {}
        body['credentials'] = self._creds
        try:
            r = requests.post('{host}/api/{api_version}/auth/signin'
                .format(host=self.host, api_version=self._api_version), json = body)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.exception("Failed to log in: {}".format(e))
            raise e
        xml_response = ET.fromstring(r.text)
        if 'token' not in xml_response[0].attrib:
            raise ValueError('Login to Tableau server failed. XML response: {}'
                .format(r.text))
        self._token = xml_response[0].attrib['token']
        logger.info('New token obtained')

    @property
    def token(self):
        if not self._token:
            self._setup()

        return self._token

    def refresh(self):
        self._setup()

class TableauMetricsCollector(object):
    '''collection of metrics for prometheus'''
    def __init__(self, token_manager, verify_ssl=False):
        logger.info('Initializing metrics collector')
        self.token_manager = token_manager
        self.verify_ssl = verify_ssl

    def collect(self):
        '''collect metrics'''
        now = datetime.datetime.now()
        print(now)
        check = '{}/admin/systeminfo.xml'.format(self.token_manager.host)

        # 3 retries
        for i in range(0,3):
            x = requests.get(check, headers={
                "Cookie": 'workgroup_session_id={}'.format(self.token_manager.token)
                }, verify=self.verify_ssl)
            xml_response = ET.fromstring(x.text)

            if 'error' == xml_response.tag:
                if 'code' == xml_response[0].tag and '1' == xml_response[0].text:
                    logger.info('Access Denied, requesting token refresh')
                    self.token_manager.refresh()
                else:
                    raise ValueError('Status check failed. XML response: {}'.format(x.text))
            else:
                # response looks good
                break
        else:
            # refreshed token 3 times, no luck
            raise ValueError('Status check failed. XML response: {}'.format(x.text))

        yield TableauServerStatusParser.tableau_server_parse_status_metrics(xml_response[0])

    def describe(self):
        return []


def start_webserver(conf):

    token_manager = TokenManager(
        conf.get('tableau_user'), conf.get('tableau_password'), conf['site'], conf['server_host'], conf['api_version'],
        token_name=conf.get('tableau_token_name'), token_secret=conf.get('tableau_token_secret'))
    REGISTRY.register(TableauMetricsCollector(token_manager, verify_ssl=conf.get('verify_ssl', False)))

    # Start up the server to expose the metrics.
    root = Resource()
    root.putChild(b'metrics', MetricsResource())

    factory = Site(root)
    logger.info('Starting webserver on {}'.format(conf['exporter_port']))
    reactor.listenTCP(conf['exporter_port'], factory)
    reactor.run()
