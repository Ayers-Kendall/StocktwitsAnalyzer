# ---------------------------------------------------------------------------------- #
# Contains methods to obtain historic data as well as general ticker information
# Created by Kendall Ayers (kendallayers4@gmail.com) on Aug 04, 2019
# ---------------------------------------------------------------------------------- #
import yfinance as yf
from pprint import pprint
from datetime import datetime

def get_info(ticker):
    info_dict = {'open': -1, 'low': -1, 'high': -1, 'market_cap': -1, 'avg_vol': -1}
    finance_dict = {}
    attempts = 0
    while attempts < 3:
        try:
            tick = yf.Ticker(ticker)
            info = tick.info
            try:
                info_dict['market_cap'] = info['marketCap']
            except:
                info_dict['market_cap'] = 'N/A'     # TODO set to last known value from previously, or database
                #print("no valid market cap data for " + ticker)
            info_dict['avg_vol'] = info['averageDailyVolume10Day']
            # info_dict['avg_vol'] = info['averageDailyVolume3Month']
            info_dict['prev_close'] = info['regularMarketPreviousClose']
            info_dict['name'] = info['shortName']
            info_dict['time'] = datetime.fromtimestamp(info['regularMarketTime'])
            info_dict['delay'] = info['exchangeDataDelayedBy']
            info_dict['volume'] = info['regularMarketVolume']
            info_dict['open'] = info['regularMarketOpen']
            info_dict['low'] = info['regularMarketDayLow']
            info_dict['high'] = info['regularMarketDayHigh']
            try:
                info_dict['prev_earnings_date'] = datetime.fromtimestamp(info['earningsTimestamp'])
                info_dict['next_earnings_start'] = datetime.fromtimestamp(info['earningsTimestampStart'])
                info_dict['next_earnings_end'] = datetime.fromtimestamp(info['earningsTimestampEnd'])
                info_dict['eps'] = info['epsTrailingTwelveMonths']
                info_dict['predicted_eps'] = info['epsForward']
            except:
                info_dict['eps'] = 'N/A'    # TODO set to last known value from previously, or database
                info_dict['prev_earnings_date'] = 'N/A' #TODO
                info_dict['next_earnings_start'] = 'N/A' #TODO
                info_dict['next_earnings_end'] = 'N/A' #TODO
                info_dict['predicted_eps'] = 'N/A' #TODO
                #print("no valid earnings data for " + ticker)
            return info_dict
        except:
            print("trying to read info/historic data again for " + ticker)
            pass
        attempts += 1
    return -1

def get_financials(ticker):
    finance_dict = {}
    attempts = 0
    while attempts < 3:
        try:
            tick = yf.Ticker(ticker)
            finance_dict['financials'] = tick.financials
            finance_dict['balance_sheet'] = tick.balance_sheet
            finance_dict['cashflow'] = tick.cashflow
            return finance_dict
        except:
            attempts += 1
    return -1

def get_historic_data():
    pass
    # TODO if necessary

get_info("AAPL")