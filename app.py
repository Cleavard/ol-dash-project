import requests
import csv
import pandas as pd
import urllib.parse as url_parse

from dash import Dash, html, dcc
import plotly.express as px

uk_url = "https://www.ons.gov.uk/generator?format={format}&uri={uri}".format(format = "csv", uri = "/economy/inflationandpriceindices/timeseries/l522/mm23")
au_url = "https://api.data.abs.gov.au/data/CPI/1.10001.10.50.Q?format={format}".format(format = "csv")

# Retrieve and process uk data
uk_dataframe = pd.read_csv(uk_url, storage_options={'User-Agent': 'Mozilla/5.0'})
uk_dataframe = uk_dataframe.rename(columns={"CPIH INDEX 00: ALL ITEMS 2015=100": "OBS_VALUE", "Title": "TIME_PERIOD"})
uk_dataframe = uk_dataframe[uk_dataframe["TIME_PERIOD"].str.contains('Q')]
uk_dataframe["TIME_PERIOD"] = uk_dataframe["TIME_PERIOD"].str.replace(' ','-')
uk_dataframe[['YEAR', 'QUARTER']] = uk_dataframe["TIME_PERIOD"].str.split('-', n=1, expand=True)
uk_dataframe['OBS_VALUE'] = uk_dataframe['OBS_VALUE'].astype('float')
uk_dataframe['INTEREST'] = uk_dataframe.groupby('QUARTER').apply(lambda x: ((x['OBS_VALUE'] - x['OBS_VALUE'].shift(1))/x['OBS_VALUE'].shift(1))*100).droplevel(0)

# Retrieve and process au data
au_dataframe = pd.read_csv(au_url, storage_options={'User-Agent': 'Mozilla/5.0'})
au_dataframe = au_dataframe.drop(['DATAFLOW', 'MEASURE', 'INDEX', 'TSEST', 'REGION', 'FREQ', 'UNIT_MEASURE', 'OBS_STATUS', 'DECIMALS', 'OBS_COMMENT'], axis=1)
au_dataframe = au_dataframe[au_dataframe['TIME_PERIOD'].isin(uk_dataframe['TIME_PERIOD'])]
au_dataframe[['YEAR', 'QUARTER']] = au_dataframe['TIME_PERIOD'].str.split('-', n=1, expand=True)
au_dataframe['OBS_VALUE'] = au_dataframe['OBS_VALUE'].astype('float')
au_dataframe['INTEREST'] = au_dataframe.groupby('QUARTER').apply(lambda x: ((x['OBS_VALUE'] - x['OBS_VALUE'].shift(1))/x['OBS_VALUE'].shift(1))*100).droplevel(0)


# Combine data
uk_dataframe['COUNTRY'] = 'UK'
au_dataframe['COUNTRY'] = 'AU'
combind_dataframe = pd.concat([uk_dataframe, au_dataframe], axis=0)
combind_dataframe['DATETIME'] = pd.PeriodIndex(combind_dataframe['TIME_PERIOD'], freq='Q').to_timestamp()

# Initilize Dash app and display data

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure = px.line(combind_dataframe, x='DATETIME', y='INTEREST', color='COUNTRY', hover_data='TIME_PERIOD').update_layout(xaxis_title='Date', yaxis_title='%'))
])
if __name__ == '__main__':
    app.run(debug=True)
