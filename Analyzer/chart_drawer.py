# ---------------------------------------------------------------------------------- #
# Contains methods to plot data for tickers
# Created by Kendall Ayers (kendallayers4@gmail.com) on Aug 04, 2019
# ---------------------------------------------------------------------------------- #

import plotly.graph_objs as go
import globals
from datetime import datetime

current_timerange = '2hour' # TODO in the future this could be updated as the user clicks on a timeframe button

def get_start_time(df):
    pass

def get_hour_and_minute(date):
    # date format = '%YYYY-%mm-%dd %HH:%MM:%SS')
    return date[11:16]

def draw(df, ticker, type='candle'):
    dict = {ticker: df}
    draw_multiple(dict)

def draw_multiple(ticker_data_dict, type='candle'):
    datalist = []
    count = 1

    # ----------------------- Setup overall layout first ----------------------- #
    layout = dict()
    layout['title'] = go.layout.Title(text='Realtime Data', xref='paper', x=0.5)
    layout['plot_bgcolor'] = 'rgb(000, 005, 002)'
    # TODO other options for time range
    if current_timerange == '2hour':
        ticktext = []
        hovertext = []
        tickvals = []
        full_dates = next(iter(ticker_data_dict.values()))['0. date']
        for i in range(0, len(full_dates)):
            hovertext.append('time: '+get_hour_and_minute(full_dates[i]))
            if i % 10 == 0: # TODO find first that is divisible by 10 mins and start from there
                tickvals.append(i)
                ticktext.append(get_hour_and_minute(full_dates[i]))
    elif current_timerange == '1week':
        ticktext = []
        hovertext = []
        tickvals = []
        full_dates = next(iter(ticker_data_dict.values()))['0. date']
        for i in range(0, len(full_dates)):
            hovertext.append(dict(test='testingtext',time=get_hour_and_minute(full_dates[i])))
            if i % 60 == 0:
                tickvals.append(i)
                ticktext.append(get_hour_and_minute(full_dates[i]))

    layout['xaxis'] = dict(rangeslider=dict(visible=False), gridcolor='#2A2A2A', tickvals=tickvals, ticktext=ticktext)
    layout['yaxis'] = dict(domain=[0, 0.2], showgrid=False, showticklabels=False)
    layout['yaxis2'] = dict(domain=[0.2, 1], gridcolor='#2A2A2A')
    layout['legend'] = dict(orientation='v', y=0.9, x=1, yanchor='bottom')  #, itemclick='toggleothers')
    layout['showlegend'] = True
    # layout['margin'] = dict(t=40, b=40, r=40, l=40)
    # ------------------------------------------------------------------------- #

    for ticker in ticker_data_dict:
        df = ticker_data_dict[ticker]

        colors = []
        for i in range(len(df['4. close'])):
            if i != 0:
                if df['4. close'][i] > df['4. close'][i - 1]:
                    colors.append(globals.INCREASING_COLOR)
                else:
                    colors.append(globals.DECREASING_COLOR)
            else:
                colors.append(globals.DECREASING_COLOR)

        #TODO fix clickability of legend to only show the ticker that is clicked on
        visible = True if count == 1 else 'legendonly'
        datalist.append(go.Candlestick(x=df.index.values,
                                        open=df['1. open'],
                                        high=df['2. high'],
                                        low=df['3. low'],
                                        close=df['4. close'],
                                        yaxis='y2',
                                        increasing=dict(line=dict(color=globals.INCREASING_COLOR)),
                                        decreasing=dict(line=dict(color=globals.DECREASING_COLOR)),
                                        name=ticker,
                                        legendgroup='group'+str(count),
                                        showlegend=True,
                                        hoverinfo='all',
                                        text=hovertext,
                                        visible=visible))
        datalist.append((dict(x=df.index.values, y=df['5. volume'],
                                marker=dict(color=colors),
                                type='bar',
                                yaxis='y',
                                name='Volume',
                                legendgroup='group'+str(count),
                                showlegend=False,
                                visible=visible)))
        count += 1

    fig = go.Figure(data=datalist, layout=layout)
    fig.show()