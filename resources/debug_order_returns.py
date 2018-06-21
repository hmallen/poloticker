cancel_result = {
    'success': 1,
    'amount': 1.0,
    'message': 'Order #12345678901 cancelled.'
}

buy_result = {
    'orderNumber': 12345678901,
    'resultingTrades': [
        {'amount': 1.0, 'date': '2018-06-18 01:00:00', 'rate': 3.53e-05, 'total': 0.00003530, 'tradeID': 12345678, 'type': 'buy'},
        {'amount': 1.0, 'date': '2018-06-18 01:00:00', 'rate': 3.53e-05, 'total': 0.00003530, 'tradeID': 12345678, 'type': 'buy'}
    ],
    'amountUnfilled': 0.0
}

sell_result = {
    'orderNumber': 12345678901,
    'resultingTrades': []
}

trade_history = [
  {
    'globalTradeID': 379214998,
    'tradeID': 12744848,
    'date': '2018-06-20 03:42:42',
    'rate': 3.44e-05,
    'amount': 369.22965117,
    'total': 0.0127015,
    'fee': 0.001,
    'orderNumber': 79777549682,
    'type': 'buy',
    'category': 'marginTrade'
  },
  {
    'globalTradeID': 379214299,
    'tradeID': 12744809,
    'date': '2018-06-20 03:30:14',
    'rate': 3.44e-05,
    'amount': 229.57034883,
    'total': 0.00789721,
    'fee': 0.001,
    'orderNumber': 79777549682,
    'type': 'buy',
    'category': 'marginTrade'},
  {
    'globalTradeID': 379202676,
    'tradeID': 12744418,
    'date': '2018-06-20 01:24:28',
    'rate': 3.41e-05,
    'amount': 598.8,
    'total': 0.02041908,
    'fee': 0.001,
    'orderNumber': 79616566826,
    'type': 'buy',
    'category': 'marginTrade'
  },
  {
    'globalTradeID': 379199202,
    'tradeID': 12744197,
    'date': '2018-06-20 01:07:29',
    'rate': 3.451e-05,
    'amount': 5.0,
    'total': 0.00017255,
    'fee': 0.002,
    'orderNumber': 79768111130,
    'type': 'sell',
    'category': 'exchange'
  }
]

open_orders_result = [
    {
        'orderNumber': 79845172991,
        'type': 'sell',
        'rate': 3.5e-05,
        'startingAmount': 5.0,
        'amount': 5.0,
        'total': 0.000175,
        'date': '2018-06-20 21:15:13',
        'margin': 0
    },
    {
        'orderNumber': 79845183980,
        'type': 'sell',
        'rate': 3.55e-05,
        'startingAmount': 6.0,
        'amount': 6.0,
        'total': 0.000213,
        'date': '2018-06-20 21:15:24',
        'margin': 0
    },
    {
        'orderNumber': 79845200963,
        'type': 'sell',
        'rate': 3.65e-05,
        'startingAmount': 5.0,
        'amount': 5.0,
        'total': 0.0001825,
        'date': '2018-06-20 21:15:33',
        'margin': 0
    }
]

# [{'globalTradeID': 379199202, 'tradeID': 12744197, 'currencyPair': 'BTC_STR',
#   'type': 'sell', 'rate': 3.451e-05, 'amount': 5.0, 'total': 0.00017255, 'fee': 0.002,
#   'date': '2018-06-20 01:07:29'}]

order_trades_result = [
    {
        'globalTradeID': 123456789,
        'tradeID': 12345678,
        'currencyPair': 'BTC_STR',
        'type': 'sell',
        'rate': 3.451e-05,
        'amount': 5.0,
        'total': 0.00017255,
        'fee': 0.002,
        'date': '2018-06-20 01:07:29'
    }
]
