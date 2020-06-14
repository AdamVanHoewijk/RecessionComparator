import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objs as go
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

df = get_data(Ticker)
df = all_time_high(df)
trace_close = go.Scatter(x=list(df['day']),
                         y=list(df['Percentage']),
                         name='Close',
                         line=dict(color="#f44242"))
data =[trace_close]
layout = dict(title="Stock Chart",
           showLegend=False)
fig = dict(data=data, layout=layout)

app = dash.Dash()

app.layout = html.Div([
    html.Div(html.H1(children='hello world')),
    html.Div(
        dcc.Graph(id="Stock Chart",
                  figure=fig)
    )

])

app.run_server(debug=True)