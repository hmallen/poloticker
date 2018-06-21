import logging
import os
from pprint import pprint
import sys

from poloniex import Poloniex

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    polo = Poloniex()

    market = 'BTC_STR'

    spend_amount = 0.00200000

    ob = polo.returnOrderBook(currencyPair=market)

    pprint(ob)

    bids = ob['bids']
    asks = ob['asks']

    print('BIDS:')
    pprint(bids)

    print('ASKS:')
    pprint(asks)

    ask_amount_total = 0
    ask_price_total = 0
    for ask in asks:
        ask_amount_total += ask[1]
        logger.debug('ask_amount_total: ' + str(ask_amount_total))

        ask_price_total += float(ask[0]) * ask[1]
        logger.debug('ask_price_total: ' + "{:.8f}".format(ask_price_total))

        if ask_price_total >= spend_amount:
            break

    logger.info('Ask Amount Total: ' + str(ask_amount_total))
    logger.info('Ask Price Total: ' + str(ask_price_total))
