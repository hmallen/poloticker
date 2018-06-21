import configparser
import logging
import os
import sys

from poloniex import Poloniex
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

    polo = Poloniex()
