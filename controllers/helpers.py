"""All the helpers go here."""
import requests
import pandas as pd
from time import mktime
from datetime import datetime


def retrieve_stock_info(symb):
    """
    Retrieve the info for a stock.

    :param symb: the symbol of the stock we want to get.
    :return: a dataframe with the info for the stock with the given symbol. None if the request was not succesful.
    """
    with open('data/%s.csv' % (symb), 'wb') as fi:
        response = requests.get('http://ichart.finance.yahoo.com/table.csv?s=%s' % (symb), stream=True)
        if not response.ok:
            return None
        for segment in response.iter_content(1024):
            fi.write(segment)
        df = pd.read_csv('data/%s.csv' % (symb), index_col='Date', parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['NaN'])
        df = df.rename(columns={'Adj Close': symb})
        df = df.reindex(index=df.index[::-1])
        return df.dropna()


def normalize_data(data, symb):
    """Return the normalized data."""
    return data / data.ix[0][symb]


def get_empty_df():
    """Get an empty dataframe."""
    return pd.DataFrame()


def get_api_data(endpoint_url, params, filepath, index_c='DATE'):
    """Retrieve info for an API and store it in a file."""
    with open(filepath, 'wb') as fi:
        response = requests.get(endpoint_url, stream=True, params=params)
        if not response.ok:
            print "Something went wrong."
        for segment in response.iter_content(1024):
            fi.write(segment)
    odf = pd.read_csv(filepath, parse_dates=True, index_col=index_c)
    return odf


def get_str_date():
    """Return a string for the current date."""
    return str(datetime.now())[:10]


def get_timestamp_from_date(dt):
    """Return an integer timestamp from a date string."""
    return int(mktime(datetime.strptime(dt, '%Y-%m-%d').timetuple())) * 1000
