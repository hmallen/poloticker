import argparse
import configparser
import datetime
import json
import logging
from multiprocessing.dummy import Process as Thread
import time

from poloniex import Poloniex
from pymongo import MongoClient
from slackclient import SlackClient
import websocket

config_path_default = '../config/config.ini'

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, default=config_path_default, help='Path to config file.')
parser.add_argument('-a', '--atlas', action='store_true', default=False,
                    help='Use MongoDB Atlas instead of local database.')
args = parser.parse_args()

use_mongodb_atlas = args.atlas
config_path = args.config

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TickerGenerator(object):

    def __init__(self, slack_info, mongo_ip):
        self.polo = Poloniex()

        self.db = MongoClient(mongo_uri).poloniex['ticker']

        self.db.drop()

        self.ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.ws.on_open = self.on_open

        self.slack_client = slack_info['client']

        self.slack_channel_id_alerts = slack_info['channels']['alerts'][1]
        self.slack_channel_id_exceptions = slack_info['channels']['exceptions'][1]

        self.last_update = None


    def __call__(self, market=None):
        if market:
            return self.db.find_one({'_id': market})

        return list(self.db.find())


    def on_message(self, ws, message):
        message = json.loads(message)

        #print(message)

        if 'error' in message:
            #print(message['error'])
            logger.error(message['error'])

            # SEND SLACK EXCEPTION MESSAGE HERE

            return

        if message[0] == 1002:
            if message[1] == 1:
                #print('Subscribed to ticker')
                logger.debug('Subscribed to ticker.')

                return

            if message[1] == 0:
                #print('Unsubscribed to ticker')
                logger.debug('Unsubscribed from ticker.')

                return

            data = message[2]

            self.db.update_one(
                {"id": float(data[0])},
                {"$set": {'last': float(data[1]),
                          'lowestAsk': float(data[2]),
                          'highestBid': float(data[3]),
                          'percentChange': float(data[4]),
                          'baseVolume': float(data[5]),
                          'quoteVolume': float(data[6]),
                          'isFrozen': float(data[7]),
                          'high24hr': float(data[8]),
                          'low24hr': float(data[9])
                          }},
                upsert=True)

            self.last_update = time.time()


    def on_error(self, ws, error):
        #print(error)
        logger.error(error)

        slack_message = 'Error returned from websocket connection:\n'
        slack_message += str(error)

        #slack_return = Ticker.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))


    def on_close(self, ws):
        #print("Websocket closed!")
        logger.debug('Websocket closed.')

        slack_message = 'Websocket closed.'

        #slack_return = Ticker.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))


    def on_open(self, ws):
        tick = self.polo.returnTicker()

        for market in tick:
            self.db.update_one(
                {'_id': market},
                {'$set': tick[market]},
                upsert=True)

        #print('Populated markets database with ticker data')
        logger.debug('Populated markets database with ticker data from REST API.')

        slack_message = 'MongoDB populated with REST API market ticker data.'

        #slack_return = Ticker.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))

        #self.last_update = datetime.datetime.now()

        self.ws.send(json.dumps({'command': 'subscribe',
                                 'channel': 1002}))

        slack_message = 'Subscribed to ticker websocket.'

        #slack_return = Ticker.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))


    def start(self):
        self.t = Thread(target=self.ws.run_forever)

        self.t.daemon = True

        self.t.start()

        #print('Thread started')
        logger.debug('Thread started.')

        #slack_message = 'Ticker startup initialized.'
        slack_message = '\n*_Ticker startup initialized at ' + str(datetime.datetime.now()) + '._*\n\n'

        #slack_return = Ticker.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))


    def stop(self):
        self.ws.close()

        self.t.join()

        #print('Thread joined')
        logger.debug('Thread joined.')

        slack_message = '*TICKER SHUTDOWN COMPLETED AT ' + str(datetime.datetime.now()) + '.*'

        #slack_return = Ticker.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))


    def monitor(self, timeout, alert_reset_interval=10):
        error_timeout = timeout

        error_message_sent = False

        error_message_time = None

        error_message_reset = datetime.timedelta(minutes=alert_reset_interval)

        slack_message = '*_Monitor activated._*'

        #slack_return = ticker.send_slack_alert(channel_id=slack_channel_id_alerts, message=error_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))

        while (True):
            try:
                #logger.debug('ticker.last_update: ' + str(ticker.last_update))
                #if (datetime.datetime.now() - ticker.last_update) > error_timeout:
                #if (time.time() - ticker.last_update) > error_timeout:
                if (time.time() - self.last_update) > error_timeout:
                    if error_message_sent == False:
                        error_message = '*NO TICKER DATA RECEIVED IN 30 SECONDS.*\n'
                        error_message += 'Restarting websocket connection.\n'

                        #slack_return = ticker.send_slack_alert(channel_id=slack_channel_id_alerts, message=error_message)
                        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=error_message)

                        logger.debug('slack_return: ' + str(slack_return))

                        error_message_sent = True

                        error_message_time = datetime.datetime.now()

                        logger.info('Stopping websocket connection.')

                        TickerGenerator.stop(self)

                        time.sleep(5)

                        logger.info('Restarting websocket connection.')

                        TickerGenerator.start(self)

                        time.sleep(5)

                        logger.info('Websocket connection restored.')

                        error_message += '*_Websocket connection restored._*'

                        #slack_return = ticker.send_slack_alert(channel_id=slack_channel_id_alerts, message=error_message)
                        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=error_message)

                        logger.debug('slack_return: ' + str(slack_return))

                if error_message_sent == True and (datetime.datetime.now() - error_message_time) > error_message_reset:
                    logger.info('Resetting error message sent switch to allow another alert.')

                    error_message_sent = False

                time.sleep(1)

            except Exception as e:
                logger.exception('Exception in inner loop.')
                logger.exception(e)

            except KeyboardInterrupt:
                logger.info('Exit signal raised in TickerGenerator.monitor. Breaking from monitor loop.')

                break

        slack_message = '*_Monitor deactivated._*'

        #slack_return = ticker.send_slack_alert(channel_id=slack_channel_id_alerts, message=error_message)
        slack_return = TickerGenerator.send_slack_alert(self, channel_id=self.slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))


    def send_slack_alert(self, channel_id, message):
        alert_return = {'Exception': False, 'result':{}}

        try:
            alert_return['result'] = slack_client.api_call(
                'chat.postMessage',
                channel=channel_id,
                text=message,
                username=slack_bot_user,
                icon_url=slack_bot_icon
            )

        except Exception as e:
            logger.exception('Exception raised in TickerGenerator.send_slack_alert().')
            logger.exception(e)

            alert_return['Exception'] = True

        finally:
            return alert_return


class Ticker:

    def __init__(self, mongo_ip):
        self.db = MongoClient(mongo_ip).poloniex['ticker']


    def __call__(self, market=None):
        if market:
            return self.db.find_one({'_id': market})

        return list(self.db.find())


if __name__ == "__main__":
    try:
        config = configparser.ConfigParser()
        config.read(config_path)

        slack_token = config['slack']['token']
        slack_channel_alerts = config['slack']['channel_alerts']
        slack_channel_exceptions = config['slack']['channel_exceptions']
        slack_bot_user = config['slack']['bot_user']
        slack_bot_icon = config['slack']['bot_icon']

        logger.info('Initializing Slack client.')

        # Slack connection
        slack_client = SlackClient(slack_token)

        channel_list = slack_client.api_call('channels.list')
        group_list = slack_client.api_call('groups.list')

        slack_channel_targets = {'alerts': slack_channel_alerts,
                                 'exceptions': slack_channel_exceptions}

        for target in slack_channel_targets:
            try:
                logger.debug('channel_list.get(\'ok\'): ' + str(channel_list.get('ok')))
                if channel_list.get('ok'):
                    for chan in channel_list['channels']:
                        logger.debug('chan[\'name\']: ' + chan['name'])
                        if chan['name'] == slack_channel_targets[target]:
                            if target == 'alerts':
                                slack_channel_id_alerts = chan['id']

                            elif target == 'exceptions':
                                slack_channel_id_exceptions = chan['id']

                            break
                    else:
                        logger.error('No valid Slack channel found for alert in channel list.')

                        sys.exit(1)

                else:
                    logger.error('Channel list API call failed.')

                    sys.exit(1)

            except:
                logger.debug('group_list.get(\'ok\'): ' + str(group_list.get('ok')))
                if group_list.get('ok'):
                    for group in group_list['groups']:
                        logger.debug('group[\'name\']: ' + group['name'])
                        if group['name'] == slack_channel_targets[target]:
                            if target == 'alerts':
                                slack_channel_id_alerts = group['id']

                            elif target == 'exceptions':
                                slack_channel_id_exceptions = group['id']

                            break
                    else:
                        logger.error('No valid Slack channel found for alert in group list.')

                        sys.exit(1)

                else:
                    logger.error('Group list API call failed.')

                    sys.exit(1)

        logger.info('Slack channel for alerts: #' + slack_channel_alerts +
                    ' (' + slack_channel_id_alerts + ')')

        logger.info('Slack channel for exceptions: #' + slack_channel_exceptions +
                    ' (' + slack_channel_id_exceptions + ')')

        slack_info = dict(client=slack_client,
                          token=slack_token,
                          channels=dict(alerts=(slack_channel_alerts, slack_channel_id_alerts),
                                        exceptions=(slack_channel_exceptions, slack_channel_id_exceptions)),
                          bot=dict(user=slack_bot_user,
                                   icon=slack_bot_icon))

        logger.info('Initializing ticker.')

        # websocket.enableTrace(True)

        if use_mongodb_atlas == True:
            atlas_user = config['mongodb']['atlas_user']
            atlas_pass = config['mongodb']['atlas_pass']

            cluster_uri = config['mongodb']['uri_atlas']

            mongo_uri = 'mongodb+srv://' + atlas_user + ':' + atlas_pass + '@' + cluster_uri

        else:
            mongo_uri = config['mongodb']['uri_local']

        logger.debug('mongo_uri: ' + mongo_uri)

        #ticker = Ticker(slack_info=slack_info, mongo_ip=mongo_ip_local)
        ticker_generator = TickerGenerator(slack_info=slack_info, mongo_ip=mongo_uri)

        #logger.info('Starting ticker thread.')
        logger.info('Starting ticker generator in separate thread.')

        #ticker.start()
        ticker_generator.start()

        #logger.info('Waiting for ticker to be ready.')
        logger.info('Waiting for ticker generator to be ready.')

        #while ticker.last_update == None:
        while ticker_generator.last_update == None:
            #logger.debug('ticker.last_update: ' + str(ticker.last_update))
            logger.debug('ticker_generator.last_update: ' + str(ticker_generator.last_update))

            time.sleep(1)

        #logger.debug('ticker.last_update: ' + str(ticker.last_update))
        logger.debug('ticker_generator.last_update: ' + str(ticker_generator.last_update))

        #last_update = ticker.last_update
        last_update = ticker_generator.last_update

        if use_mongodb_atlas == True:
            mongo_uri_preview = 'on MongoDB Atlas cluster:\n_mongodb+srv://{ATLAS_USER}:{ATLAS_PASS}@' + cluster_uri + '_'

        else:
            if mongo_uri.split('.')[0].split('/')[-1] == '192':
                location = 'local'
            else:
                location = 'remote'

            mongo_uri_preview = 'at ' + location + ' IP:\n' + mongo_uri + ''

        slack_message = 'Real-time Poloniex ticker data ready for use ' + mongo_uri_preview

        #slack_return = ticker.send_slack_alert(channel_id=slack_channel_id_alerts, message=slack_message)
        slack_return = ticker_generator.send_slack_alert(channel_id=slack_channel_id_alerts, message=slack_message)

        logger.debug('slack_return: ' + str(slack_return))

        logger.info('Starting monitor.')

        #ticker.monitor(timeout=30, alert_reset_interval=10)
        ticker_generator.monitor(timeout=30, alert_reset_interval=10)

        #logger.info('Exited inner loop.')
        logger.info('Exited monitor.')

    except Exception as e:
        logger.exception('Exception in outer loop.')
        logger.exception(e)

    except KeyboardInterrupt:
        logger.info('Exit signal raised in outer try/except.')

    finally:
        logger.info('Shutting down ticker.')

        #ticker.stop()
        ticker_generator.stop()

        logger.info('Exiting.')
