"""All the helpers go here."""
import json
import requests
import pandas as pd
from time import mktime
from config.config import endpoints
from datetime import datetime, timedelta

cached_stocks = {}


def retrieve_stock_info(symb):
    """Retrieve the info for a stock.

    :param symb: the symbol of the stock we want to get.
    :return: a dataframe with the info for the stock with the given symbol. None if the request was not succesful.
    """
    index_string = '%s-%s' % (symb, get_str_date())
    if index_string in cached_stocks:
        return cached_stocks[index_string]
    with open('data/%s.csv' % (symb), 'wb') as fi:
        query_url = endpoints['alpha-vantage']['base_url']
        params = endpoints['alpha-vantage']['params']
        params['symbol'] = symb
        response = requests.get(query_url, params=params, stream=True)
        if not response.ok:
            return None
        print response.url
        for segment in response.iter_content(1024):
            fi.write(segment.decode('utf-8-sig'))
    df = pd.read_csv('data/%s.csv' % (symb),
                     index_col='timestamp',
                     parse_dates=True,
                     na_values=['NaN'],
                     usecols=['timestamp', 'adjusted_close'])
    print df.columns
    df = df.rename(columns={'adjusted_close': symb, 'timestamp': 'Date'})
    df = df.reindex(index=df.index[::-1])
    df = df.dropna()
    cached_stocks[index_string] = df
    return df


def normalize_data(data):
    """Return the normalized data."""
    return data / data.ix[0]


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


def get_query_related_tickers(term):
    """Query Yahoo Finance to get search suggestions."""
    result_set = []
    endpoint = endpoints['yhoo-search']
    query_url = endpoint['base_url'] + term
    r = requests.get(query_url, params=endpoint['params'])
    if r.status_code == 200:
        js_obj = json.loads(r.text)
        suggestions = js_obj['data']['items']
        result_set = ["%s(%s) - %s" % (k['name'], k['symbol'], k['exchDisp']) for
                      k in suggestions if k['exchDisp'] in ('NASDAQ', 'NYSE')]
    return result_set


def get_subset_dates(data, begin_date=None, end_date=None):
    """Return the data within the given dates."""
    reass = False
    if type(begin_date) is str:
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
    if type(end_date) is str:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    if begin_date > end_date:
        raise Exception('Invalid date range.')
    if begin_date is None:
        reass = True
        begin_date = data.index[0]
    if end_date is None:
        reass = True
        end_date = data.index[-1]
    try:
        bd2 = pd.Timestamp(begin_date)
        if not reass:
            return data.ix[: bd2]
        return data
    except Exception:
        ix = data.index
        if begin_date not in ix:
            changed = False
            for i in range(1, 6):
                if begin_date + timedelta(days=i) in ix:
                    begin_date += timedelta(days=i)
                    changed = True
                    break
            if not changed:
                begin_date = ix[0]
        if end_date not in ix:
            changed = False
            for i in range(1, 6):
                if end_date - timedelta(days=i) in ix:
                    end_date -= timedelta(days=i)
                    changed = True
                    break
            if not changed:
                end_date = ix[-1]
        bd2 = pd.Timestamp(begin_date)
        return data.ix[: bd2]
