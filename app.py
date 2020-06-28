import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objs as go
import plotly.express as px
from pandas_datareader._utils import RemoteDataError
from pandas_datareader import data

START_DATE = '2020-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')
Ticker = '^GSPC'


# Return a data frame with only the values after a all time high
def all_time_high(df):
    maxDate = datetime.now()
    maxClose = 0.0
    for ind in df.index:
        loopval = df['Adj Close'][ind]
        if loopval > maxClose:
            maxClose = loopval
            maxDate = ind
    df = df.drop(df[df.index < maxDate].index)

    df['Percentage'] = df['Adj Close'] / maxClose - 1
    df['day'] = np.arange(len(df))
    return df


# Select the adjusted closed, fills nill and makdes sure the dates are within range
def clean_data(df):
    dateRange = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = df['Adj Close'].reindex(dateRange)
    return clean_data.fillna(method='ffill').to_frame()


# Collects ticker data from yahoo and returns it cleaned
def get_data(ticker):
    try:
        df = data.DataReader(ticker,
                             'yahoo',
                             START_DATE,
                             END_DATE)
        return clean_data(df)

    except RemoteDataError:
        print('no data Found for {t}'.format(t=ticker))


def current_df():
    df = get_data(Ticker)
    df = all_time_high(df)
    df['Res'] = 'Current'
    return df


def merged_fig(df_name, current_df):
    max_day = current_df[current_df['day'] == current_df['day'].max()].iloc[0]['day']
    df = pd.read_csv(df_name, index_col='Date')
    df = df.drop(df[df.day > max_day * 3].index)
    return px.line(pd.concat([df, current_df]), x="day", y="Percentage", color='Res')


gd_fig = merged_fig('The great depression.csv', current_df())

app = dash.Dash()

app.layout = html.Div([
    html.H1(children='Current percentage change of S&P500 displayed alongside historical change'),
    html.Button('The great depression', id='gd_button'),
    dcc.Graph(figure=gd_fig,
              id='graph')


app.run_server(debug=True)
