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

uk_dataframe[['YEAR', 'QUARTER']] = df['TIME_PERIOD'].str.split('_', n=1)
uk_dataframe['YEAR'] = uk_dataframe.['YEAR'],astype('int')

uk_dataframe.set_index(['YEAR', 'QUARTER'], inplace=True)
uk_dataframe['INTEREST'] = np.na

for index, row in uk_dataframe.iterrows():
    try:
        previous_year_ = uk_dataframe.loc[index['YEAR']-1, index['QUARTER']]

    except KeyError:
        continue