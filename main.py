from secret import API_KEY, API_SECRET, BASE_URL
import alpaca_trade_api as tradeapi
import time 



api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL, api_version='v2')

symbol = 'AAPL'

# Define your trading strategy parameters
short_window = 50  # Short-term SMA
long_window = 200  # Long-term SMA

# Initialize variables
in_position = False

while True:
    # Get historical data
    barset = api.get_barset(symbol, 'day', limit=long_window)
    bars = barset[symbol]

    if len(bars) < long_window:
        print('Not enough data to compute moving averages. Waiting...')
        time.sleep(3600)  # Sleep for 1 hour and try again
        continue

    # Calculate short-term and long-term SMAs
    short_sma = sum(bar.c for bar in bars[-short_window:]) / short_window
    long_sma = sum(bar.c for bar in bars) / long_window

    # Get the current account information
    account = api.get_account()
    cash = float(account.cash)

    if short_sma > long_sma and not in_position:
        # Buy signal
        print(f'Buy {symbol} at {bars[-1].c}')
        api.submit_order(
            symbol=symbol,
            qty=int(cash / bars[-1].c),
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        in_position = True
    elif short_sma < long_sma and in_position:
        # Sell signal
        print(f'Sell {symbol} at {bars[-1].c}')
        api.submit_order(
            symbol=symbol,
            qty=int(cash / bars[-1].c),
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        in_position = False

    time.sleep(3600)  # Sleep for 1 hour before checking again





