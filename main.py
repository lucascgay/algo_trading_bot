from secret import API_KEY, API_SECRET, BASE_URL
import alpaca_trade_api as tradeapi

api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL, api_version='v2')

print(api.get_account())