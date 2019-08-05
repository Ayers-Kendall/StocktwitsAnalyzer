# ---------------------------------------------------------------------------------- #
# Contains methods to analyze stocktwits trending tickers and user posts
# And allows the tickers to then be further analyzed
# Created by Kendall Ayers (kendallayers4@gmail.com) on Aug 04, 2019
# ---------------------------------------------------------------------------------- #

import time
import datetime
import pandas
import pytwits

def getTrending():
    access_token = 'TOKEN'
    stocktwits = pytwits.StockTwits()  # access_token=access_token <-- parameter if authorized account made
    symbols = stocktwits.trending(path='symbols')
    symbol_list = []
    for symbol in symbols:
        symbol_list.append(symbol.symbol)
    return symbol_list

old_trending = []
def check_new_trending():
    global old_trending
    new_trending = getTrending()
    # compare to see if any new stocks are trending
    for ticker in new_trending:
        if not any(ticker == old for old in old_trending):
            # TODO check ticker to see if it looks like a good buy
            pass
    old_trending = new_trending

def check_all_trending():
    global old_trending
    for ticker in old_trending:
        # TODO check ticker to see if it looks like a good buy and add to some global list
        pass

end_of_day_accuracy_checks = {}
def analyze_posts(posts, username=None):
    global end_of_day_accuracy_checks
    ticker_predictions = {}
    for post in posts:
        # TODO Determine which tickers this username is bullish or bearish about and store in format pred = {'TICK': 'bull/bear'}
        ticker_predictions['CHANGE TO FOUND TICK VARIABLE'] = 'bull/bear CHANGE TO FOUND RESULT'
        pass
    if username in end_of_day_accuracy_checks:
        for pred in ticker_predictions:
            end_of_day_accuracy_checks[username][pred] = ticker_predictions[pred]
    elif username != None:
        end_of_day_accuracy_checks[username] = ticker_predictions
    return ticker_predictions

def check_whitelist_posts():
    whitelist = pandas.read_csv("whitelist.csv")
    for i, row in whitelist.iterrows():
        if row['% accuracy'] > 50:
            check_user_posts(row['username'])

def check_user_posts(username):
    stocktwits = pytwits.StockTwits()  # access_token=access_token <-- parameter if authorized account made
    user, cursor, messages = stocktwits.streams(path='user', id=username)
    predictions = analyze_posts(messages, username)
    # TODO further analyze predictions and provide info to user

def check_ticker_posts(ticker):
    stocktwits = pytwits.StockTwits()  # access_token=access_token <-- parameter if authorized account made
    symbol, cursor, messages = stocktwits.streams(path='symbol', id=ticker, limit=30)
    predictions = analyze_posts(messages, None)
    # TODO further analyze predictions and provide info to user

def check_user_accuracy():
    global end_of_day_accuracy_checks
    # TODO
    # Loop through and create list of tickers to check

    # use realtime_data.get_batch(ticker_list)

    # Loop through and determine accuracy

        # Update accuracy to csv file


def main():
    minutes = 0
    while True:
        # TODO
        # Add time checks so this only runs the functions during the market day, but continuously runs for server use
        # TODO
        try:
            check_new_trending()
            if minutes % 30 == 0 and minutes != 0:
                check_all_trending()
            if minutes % 5 == 0:
                check_whitelist_posts()
            minutes += 1
            time.sleep(60)
            # If it is after market close and a weekday, check the users accuracy and update vals
            # TODO check for market holidays (create market_open() function returning true or false)
            if datetime.datetime.now().hour == 16 and datetime.datetime.now().isoweekday() <= 5:
                check_user_accuracy()
            while datetime.datetime.now().hour != 9 or datetime.datetime.now().isoweekday() > 5:
                time.sleep(900) # Wait for next trading day
        except:
            time.sleep(60)
            pass

if __name__ == '__main__':
    main()
