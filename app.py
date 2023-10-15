import requests
import csv
import pandas as pd
import urllib.parse as url_parse

uk_inflation_rates = {}

uk_url = "https://www.ons.gov.uk/generator?format={format}&uri={uri}".format(format = "csv", uri = "/economy/inflationandpriceindices/timeseries/l522/mm23")

au_url = "https://api.data.abs.gov.au/data/CPI/1.10001.10.50.Q?format={format}".format(format = "csv")

print(uk_url)

uk_dataframe = pd.read_csv(uk_url, storage_options={'User-Agent': 'Mozilla/5.0'})
uk_dataframe = uk_dataframe.rename(columns={"CPIH INDEX 00: ALL ITEMS 2015=100": "OBS_VALUE", "Title": "TITLE"})
uk_dataframe = uk_dataframe[uk_dataframe["TITLE"].str.contains('Q')]
uk_dataframe[['YEAR', 'QUARTER']] = uk_dataframe['TITLE'].str.split(" ", n=1, expand=True)
uk_dataframe = uk_dataframe.drop(['TITLE'], axis=1)
uk_dataframe['YEAR'] = uk_dataframe['YEAR'].astype('int')
uk_dataframe['OBS_VALUE'] = uk_dataframe['OBS_VALUE'].astype('float')

uk_dataframe['INTEREST'] = uk_dataframe.groupby('QUARTER').apply(lambda x: (x['OBS_VALUE'] - x['OBS_VALUE'].shift(1))/x['OBS_VALUE'].shift(1)).droplevel(0)

print(uk_dataframe.to_string())

'''
uk_dataframe[['YEAR', 'QUARTER']] = uk_dataframe['TIME_PERIOD'].str.split('_', n=1)
uk_dataframe['YEAR'] = uk_dataframe['YEAR'],astype('int')


uk_dataframe.loc[uk_dataframe.groupby('QUARTER')['INTEREST'].iloc[1:].index, 'INTEREST'] = 0

print(uk_dataframe.to_string())
'''