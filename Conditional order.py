import ccxt
from pprint import pprint
import api_confing_my_bybit as ac
import time
from datetime import datetime
import pandas as pd


exchange = ccxt.bybit({
    'options': {
        'adjustForTimeDifference': True,
    },
    'apiKey': ac.API_KEY,
    'secret': ac.SECRET_KEY,
    'password': ac.PASSWORD,
})

print(exchange)

symbol = 'BTC/USDT:USDT'  # my symbol
amount = 0.001  # size
price = 25000  # enty price
sl = 24000  # stop price
tp = 33000  # profit price
type = 'limit'
sl_tk = {
    'stop_loss': sl,  # stop price
    'type': 'stopMarket',
    'take_profit': tp,  # profit price
}


run = True  # while Condition
sleep_time = 10  # sleep time for while
counter = 0  # Counter


global in_position
in_position = False  # position Check

while run == True:
    pprint('------------------')
    pprint('bot is working')
    pprint('------------------')
    print(f"Fetching new bars for {datetime.now().isoformat()}")
    bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=5)  # fetch ohlcv
    df = pd.DataFrame(bars[:-1], columns=['timestamp',
                      'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    print(df)
    pprint('------------------')
    time.sleep(2)

    # create order Condition
    df.loc[df['close'] > df['open'], 'sig'] = 'create'
    # cancel order Condition
    df.loc[df['close'] < df['open'], 'sig'] = 'cancel'

    sig = df.iloc[-1]['sig']

    if sig == 'create':  # Check for create order
        pprint('open order Condition is true')
        pprint('------------------')
        time.sleep(2)
        if not in_position:  # Check for create open positions
            order = exchange.create_limit_buy_order(  # create limit buy order
                symbol, amount, price, params=sl_tk)
            pprint('bot made your order ')
            in_position = True
            counter = counter + 1
            pprint('------------------')
            print(f'Number of positions : ‌‌{(counter)}')

        else:
            pprint('already in position')

    if sig == 'cancel':  # Check for cancel order
        pprint('cancel order Condition is true')
        pprint('------------------')
        time.sleep(1)
        if in_position:  # Check for create open positions
            cancel_order = exchange.cancel_all_orders(
                symbol)  # cancel limit buy order
            pprint('bot cancel your order ')
            in_position = False
        else:
            pprint('You are not in position')

    time.sleep(sleep_time)
