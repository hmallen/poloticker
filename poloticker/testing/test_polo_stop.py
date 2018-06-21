import configparser
import logging
import os
from pprint import pprint
import sys

import requests

config_path = '../../config/config.ini'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(config_path)

    api = config['poloniex']['api']
    secret = config['poloniex']['secret']

    auth_headers = {'Key': api, 'Sign': secret}

    polo_endpoint_trading = 'https://poloniex.com/tradingApi/'

    polo_endpoint = polo_endpoint_trading + 'returnOpenOrders'

    r = requests.post(polo_endpoint, headers=auth_headers)

    pprint(r)

    result = r.json()

    pprint(result)
