import requests
import csv
import pandas as pd
import urllib.parse as url_parse

uk_inflation_rates = {}

uk_url = "https://www.ons.gov.uk/generator?format={format}&uri={uri}".format(format = "csv", uri = "/economy/inflationandpriceindices/timeseries/l522/mm23")

au_url = "https://api.data.abs.gov.au/data/CPI/1.10001.10.50.Q?format={format}".format(format = "csv")

# Retrieve and process uk data
uk_dataframe = pd.read_csv(uk_url, storage_options={'User-Agent': 'Mozilla/5.0'})
uk_dataframe = uk_dataframe.rename(columns={"CPIH INDEX 00: ALL ITEMS 2015=100": "OBS_VALUE", "Title": "TITLE"})
uk_dataframe = uk_dataframe[uk_dataframe["TITLE"].str.contains('Q')]
uk_dataframe[['YEAR', 'QUARTER']] = uk_dataframe['TITLE'].str.split(" ", n=1, expand=True)
uk_dataframe = uk_dataframe.drop(['TITLE'], axis=1)
uk_dataframe['YEAR'] = uk_dataframe['YEAR'].astype('int')
uk_dataframe['OBS_VALUE'] = uk_dataframe['OBS_VALUE'].astype('float')
uk_dataframe['INTEREST'] = uk_dataframe.groupby('QUARTER').apply(lambda x: (x['OBS_VALUE'] - x['OBS_VALUE'].shift(1))/x['OBS_VALUE'].shift(1)).droplevel(0)

# Retrieve and process au data
au_dataframe = pd.read_csv(au_url, storage_options={'User-Agent': 'Mozilla/5.0'})
au_dataframe = au_dataframe.drop(['DATAFLOW', 'MEASURE', 'INDEX', 'TSEST', 'REGION', 'FREQ', 'UNIT_MEASURE', 'OBS_STATUS', 'DECIMALS', 'OBS_COMMENT'], axis=1)
au_dataframe[['YEAR', 'QUARTER']] = au_dataframe['TIME_PERIOD'].str.split("-", n=1, expand=True)
au_dataframe = au_dataframe.drop(['TIME_PERIOD'], axis=1)
au_dataframe['YEAR'] = au_dataframe['YEAR'].astype('int')
au_dataframe['OBS_VALUE'] = au_dataframe['OBS_VALUE'].astype('float')
au_dataframe['INTEREST'] = au_dataframe.groupby('QUARTER').apply(lambda x: (x['OBS_VALUE'] - x['OBS_VALUE'].shift(1))/x['OBS_VALUE'].shift(1)).droplevel(0)

