# ---------------------------------------------------------------------------------- #
# Contains methods to obtain realtime technical indicators
# Created by Kendall Ayers (kendallayers4@gmail.com) on Aug 04, 2019
# ---------------------------------------------------------------------------------- #

# AlphaVantage has an API for technical indicators, but to save API calls, let's use the TA-Lib package

import historic_data
from alpha_vantage.techindicators import TechIndicators
import talib

ti = TechIndicators(key='ANWQLLVPMN08AOI5', output_format='pandas', indexing_type='date')

# dict of functions sorted by group -- for more function detail see https://github.com/mrjbq7/ta-lib
groups = talib.get_function_groups()
for group in groups:
    print(group + ' : ' + str(groups[group]))

#TODO Find out which indicators and which pattern recognition functions (CDL...) are most important
def check_major_indicators(df):
    pass

def check_major_patterns(df):
    pass

def get_SMA():
    pass