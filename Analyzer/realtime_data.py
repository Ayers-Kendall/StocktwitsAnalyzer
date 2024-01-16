# ---------------------------------------------------------------------------------- #
# Contains methods to obtain realtime data
# Created by Kendall Ayers (kendallayers4@gmail.com) on Aug 04, 2019
# ---------------------------------------------------------------------------------- #

import historic_data
from alpha_vantage.timeseries import TimeSeries
import time
import globals
import pandas

ts = TimeSeries(key=globals.ALPHA_VANTAGE_API_KEYS[0], output_format='pandas', indexing_type='date')
#ts2 = TimeSeries(key=globals.ALPHA_VANTAGE_API_KEYS[1], output_format='pandas', indexing_type='date')

def reindex_data(df):
    df['0. date'] = df.index
    indexes = []
    for i in range(0, len(df)):
        indexes.append(i)
    df.index = indexes
    return df

def average(lst):
    return sum(lst) / len(lst)

def get_data(ticker, size='compact', interval='1min'): # size 'compact' = last 100 data points, 'full' = max that API will give
    info = historic_data.get_info(ticker)
    market_cap = info['market_cap']
    day_low = info['low']
    day_high = info['high']
    day_open = info['open']
    prev_close = info['prev_close']
    current_quote = {'price': "N/A", 'percent_change': "N/A", 'vol/avg': "N/A", 'day_low': day_low, 'day_high': day_high, 'market_cap': market_cap, 'ticker': ticker}
    data, meta_data = ts.get_intraday(symbol=ticker, interval=interval, outputsize=size)
    current_quote['price'] = data['4. close'][-1]
    current_quote['percent_change'] = ((current_quote['price'] / prev_close) - 1 ) * 100
    avg_vol_1min = average(data['5. volume'])
    current_quote['vol/avg'] = data['5. volume'][-1] / avg_vol_1min
    modified_data = reindex_data(data)
    globals.alpha_vantage_api_call_count += 1
    return current_quote, modified_data

# Returns full minutely seperated data for each ticker in the batch as a dict {tick: data, ...}
def get_batch_data(ticker_list):
    ticker_data_dict = {}
    for ticker in ticker_list:
        ticker_data_dict[ticker] = get_data(ticker)[1]
        globals.alpha_vantage_api_call_count += 1
        time.sleep(12)
    return ticker_data_dict

# Returns a single price quote for every ticker in the list, but only costs 1 API call
# Will ignore invalid tickers :)
def get_batch_quotes(ticker_list, ts=ts):
    try:
        data, meta_data = ts.get_batch_stock_quotes(symbols=ticker_list)
    except Exception as e:
        print(e)
        return -1
    #pprint(data)
    quotes = []
    for index, row in data.iterrows():
        ticker = row['1. symbol']
        info = historic_data.get_info(ticker)
        try:
            market_cap = info['market_cap']
            day_low = info['low']
            day_high = info['high']
            day_open = info['open']
            prev_close = info['prev_close']
            avg_vol = info['avg_vol']
        except:
            market_cap = -1
            day_low = -1
            day_high = -1
            day_open = -1
            prev_close = -1
            avg_min_vol = -1
        current_quote = {'price': "N/A", 'percent_change': "N/A", 'vol/avg': "N/A", 'day_low': day_low, 'day_high': day_high, 'market_cap': market_cap, 'ticker': ticker}
        current_quote['price'] = row['2. price']
        current_quote['percent_change'] = ((float(current_quote['price']) / prev_close) - 1) * 100
        try:
            current_quote['vol/avg'] = float(row['3. volume']) / float(avg_vol)   # Only works during market day (volume is '--' after)
        except Exception as e:
            print(e)
            current_quote['vol/avg'] = 'N/A'
        quotes.append(current_quote)
    globals.alpha_vantage_api_call_count += 1
    return quotes




# ----------- Everything below this point is for testing various APIs for other real time data sources ------------ #




def get_data_intrinio(ticker):
    import intrinio_sdk
    from pprint import pprint
    from intrinio_sdk.rest import ApiException

    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = globals.INTRINIO_API_KEYS[0]
    security_api = intrinio_sdk.SecurityApi()
    identifier = ticker  # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)

    try:
        start_date = '2019-08-01'  # date | Return intraday prices starting at the specified date (optional)
        end_date = '2019-08-04'  # date | Return intraday prices stopping at the specified date (optional)
        api_response1 = security_api.get_security_realtime_price(identifier, start_date=start_date, end_date=end_date)
        api_response2= security_api.get_security_realtime_price(identifier)#, start_date=start_date, end_date=end_date)
        pprint(api_response1)
        pprint(api_response2)
    except ApiException as e:
        print("Exception when calling SecurityApi->get_security_intraday_prices: %s\n" % e)

def get_data_iex(ticker):
    from iexfinance.account import get_usage
    print(get_usage(quota_type='messages', token=globals.IEX_SECRET_KEY))
    from iexfinance.altdata import get_social_sentiment
    #print(get_social_sentiment("AAPL", token=globals.IEX_SECRET_KEY))
    from iexfinance.stocks import Stock
    #aapl = Stock("AAPL", token=globals.IEX_SECRET_KEY)
    #print(aapl.get_estimates())
    #print(aapl.get_price_target())
    from datetime import datetime
    from iexfinance.stocks import get_historical_intraday
    #date = datetime(2018, 11, 27)
    #get_historical_intraday("AAPL", date)
    df = get_historical_intraday("AAPL", output_format='pandas', token=globals.IEX_SECRET_KEY)   # Can go up to 3 months back minutely
    print(df)
    # REAL TIME
    from iexfinance.stocks import Stock
    tsla = Stock('TSLA', token=globals.IEX_SECRET_KEY)  # CAUSING ERROR, maybe because the market isn't open now??
    tsla.get_price()
    batch = Stock(["TSLA", "AAPL"], token=globals.IEX_SECRET_KEY)
    batch.get_price()

def get_data_wtc(ticker_list):      # 250 calls a day, and can get 5 tickers in one call :( website says 500 per call. Only $16 a month for 50,000 and 50 per
    import json, requests
    from pprint import pprint
    __wtc_base_URL = 'https://api.worldtradingdata.com/api/v1/'
    __wtc_token = globals.WTC_API_KEY
    tickers_string = ''
    for ticker in ticker_list:
        tickers_string += str(ticker) + ','
    tickers_string = tickers_string[:-1]    # get rid of comma at the end
    response = requests.get(__wtc_base_URL + "stock?symbol=" + tickers_string + '&api_token='+__wtc_token, timeout=60)
    if response.status_code == 200:
        res_json = json.loads(response.content.decode('utf-8'))
        for ticker_data in res_json['data']:
            print(ticker_data)
    else:
        print('None')



#import chart_drawer
#ticker_list = ['AAPL', 'MSFT', 'GPRO', 'UVXY', 'AMZN', 'GOOG']
#data_dict = get_batch_data(ticker_list)
#chart_drawer.draw_multiple(data_dict)
#chart_drawer.draw(get_data("AAPL")[1], "AAPL")
#get_data_iex("AAPL")
#get_data_wtc(["AAPL", "AMZN", "GOOG", "UVXY", "GPRO", "MSFT", "IBM"])
from pprint import pprint
batch = (get_batch_quotes(["AAPL", "AMZN", "GOOG", "UVXY", "GPRO", "MSFT", "IBM", "GNE", "QTRX", "ARQL", "GH", "EXAS", "SPWR",
                           "SBGL", "BAND", "EBR", "TNAV", "AXNX", "FSI", "IPHI", "ROKU", "MGTX", "CDNA", "COUP"]))
i = 0
while i < 15:
    if i % 2 == 0:
        batch = get_batch_quotes(["AAPL", "AMZN", "GOOG", "UVXY", "GPRO", "MSFT", "IBM", "GNE", "QTRX", "ARQL", "GH", "EXAS", "SPWR",
             "SBGL", "BAND", "EBR", "TNAV", "AXNX", "FSI", "IPHI", "ROKU", "MGTX", "CDNA", "COUP"])
    else:
        batch = get_batch_quotes(
            ["AAPL", "AMZN", "GOOG", "UVXY", "GPRO", "MSFT", "IBM", "GNE", "QTRX", "ARQL", "GH", "EXAS", "SPWR",
             "SBGL", "BAND", "EBR", "TNAV", "AXNX", "FSI", "IPHI", "ROKU", "MGTX", "CDNA", "COUP"], ts=ts2)
    print(i)
    i += 1

#for quote in batch:
#    print(quote)
