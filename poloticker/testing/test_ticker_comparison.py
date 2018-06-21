import configparser
import logging
import os
import sys
import time

from poloniex import Poloniex
import requests
from ticker import Ticker

config_path = '../../config/config.ini'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(config_path)

    api = config['poloniex']['api']
    secret = config['poloniex']['secret']

    polo = Poloniex()

    ticker = Ticker('mongodb://192.168.1.179:27017/')

    while (True):
        print(ticker('BTC_STR')['last'], polo.returnTicker()['BTC_STR']['last'])

        time.sleep(1)
