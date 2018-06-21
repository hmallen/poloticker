import argparse
import configparser
import datetime
import json
import logging
from multiprocessing.dummy import Process as Thread
import time

from poloniex import Poloniex
import websocket

config_path_default = '../../config/config.ini'

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, default=config_path_default, help='Path to config file.')
args = parser.parse_args()

config_path = args.config

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PoloWebsocket:

    def __init__(self):
        self.api = Poloniex()

        self.ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.ws.on_open = self.on_open


    def on_message(self, ws, message):
        message = json.loads(message)

        logger.debug('message: ' + str(message))

        if 'error' in message:
            logger.error(message['error'])

            return

        elif message[0] == 1010:
            logger.debug('Heartbeat.')

            return

        #if message[0] == 1002:
        if message[1] == 1:
            logger.debug('Subscribed to channel ' + str(message[0]) + '.')

            return

        if message[1] == 0:
            logger.debug('Unsubscribed from channel ' + str(message[0]) + '.')

            return

        #data = message[2]

        #logger.debug('data: ' + str(data))


    def on_error(self, ws, error):
        logger.error(error)


    def on_close(self, ws):
        logger.debug('Websocket closed.')


    def on_open(self, ws):
        self.ws.send(json.dumps({'command': 'subscribe',
                                 'channel': 'BTC_STR'}))


    def start(self):
        self.t = Thread(target=self.ws.run_forever)

        self.t.daemon = True

        logger.debug('Starting websocket process.')

        self.t.start()

        logger.debug('Thread started.')


    def stop(self):
        logger.debug('Terminating websocket process.')

        self.ws.close()

        self.t.join()

        logger.debug('Thread joined.')


if __name__ == "__main__":
    # websocket.enableTrace(True)

    logger.debug('Initializing PoloWebsocket.')

    pw = PoloWebsocket()

    logger.debug('Starting program.')

    pw.start()

    while (True):
        time.sleep(0.1)

    logger.info('Done.')
