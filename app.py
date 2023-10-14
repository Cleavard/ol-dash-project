import requests
import csv
import pandas as pd
import urllib.parse as url_parse

base_uk_url = "https://www.ons.gov.uk/generator/?"
uk_params = {"uri" : " /economy/inflationandpriceindices/timeseries/l522/mm23", "format" : "csv"}

base_au_url = ": https://api.data.abs.gov.au/data/CPI/1.10001.10.50.Q"
au_params = {"format" : "csv"}

uk_dataframe = pd.read_csv(base_uk_url + url_parse.urlencode(uk_params))
uk_inflation_rates = {}

uk_dataframe[['YEAR', 'QUARTER']] = uk_dataframe['TIME_PERIOD'].str.split('_', n=1)
uk_dataframe['YEAR'] = uk_dataframe.['YEAR'],astype('int')

uk_dataframe.groupby('QUARTER')['INTEREST'].apply(lambda x: (x - x.shift(1))/x.shift(1))


uk_dataframe.loc[uk_dataframe.groupby('QUARTER')['INTEREST'].iloc[1:].index, 'INTEREST'] = 0
