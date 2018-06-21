import logging
import os
from pprint import pprint
import sys
import time

from pymongo import MongoClient

mongo_ip = 'mongodb://192.168.1.179:27017/'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Returns current ticker value from MongoDB
def ticker(market=None):
    if market:
        return db.find_one({'_id': market})

    return list(db.find())


if __name__ == '__main__':
    try:
        logger.info('Connecting to MongoDB.')

        db = MongoClient(mongo_ip).poloniex['ticker']

        logger.info('Beginning ticker data acquisition and display in 5 seconds.')

        for i in range(3):
            time.sleep(5)

            #pprint(ticker('USDT_BTC'))
            pprint(ticker('BTC_STR'))
            #pprint(ticker('USDT_STR'))
            print()

        logger.info('Done.')

    except Exception as e:
        logger.exception(e)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')

    finally:
        logger.info('Exiting.')
