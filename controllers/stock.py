"""The model training, fitting, predictions, etc. goes here."""
import numpy as np
import datetime as dt
from pandas import isnull
from config.config import endpoints
from sklearn.model_selection import train_test_split
from helpers import *


class Stock(object):

    """Represents a stock object."""

    def __init__(self, symb, n_days, begin_date=None, end_date=None):
        """Create an instance of Stock."""
        if n_days == '':
            n_days = 7
        self.symb = symb
        self.original_data = retrieve_stock_info(self.symb)
        if begin_date == '':
            begin_date = None
        if end_date == '':
            end_date = None
        self.begin_date, self.end_date = begin_date, end_date
        self.data = get_subset_dates(self.original_data, begin_date=begin_date,
                                     end_date=end_date)
        self.data = normalize_data(self.data)
        self.fill_dataset()
        self.n_days = n_days

    def get_rolling_stats(self):
        """Get the rolling mean and stdev."""
        rolling = self.data.rolling(window=20, center=False)

        rm = rolling.mean().dropna()
        rstd = rolling.std().dropna()

        rolling_mean = rm[self.symb]
        rolling_std = rstd[self.symb]
        return rolling_mean, rolling_std

    def add_rolling_mean(self, rm):
        """Add the rolling mean's data to the dataset."""
        self.data['rolling_mean'] = rm

    def add_bollinger_bands(self, rstd):
        """Add the bollinger bands' data to the dataset."""
        self.data['upper_band'] = self.data['rolling_mean'] + 2 * rstd
        self.data['lower_band'] = self.data['rolling_mean'] - 2 * rstd

    def add_spy_info(self):
        """Add S&P 500's info to the dataset."""
        spy = normalize_data(retrieve_stock_info('SPY'))
        self.data = self.data.join(spy, how='inner')

    def add_beta_and_sharpe(self):
        """Calculate beta."""
        # Create a new, empty DataFrame
        temp_df = get_empty_df()

        # Store in the columns 'stock' and 'm_index' the daily returns for the
        # stock price and the market index, respectively.
        temp_df['stock'] = self.data[self.symb].shift(1) / self.data[self.symb] - 1
        temp_df['m_index'] = self.data['SPY'].shift(1) / self.data['SPY'] - 1

        # Set the return for the first date with data to 0.
        temp_df.ix[0, :] = 0

        # Array to store the values of beta
        betas = [0, 0]
        sr = []

        # Iterate over the DataFrame, calculating beta for every date and storing it in betas.
        for ix, row in enumerate(temp_df.iterrows()):
            sub_df = temp_df.ix[:ix, :]
            stdev = np.std(sub_df['stock'])
            if isnull(stdev):
                sr.append(0)
                continue
            if stdev != 0:
                sr.append(np.mean(sub_df['stock']) / stdev)
            else:
                sr.append(0)
            if ix > 1:
                betas.append(np.polyfit(sub_df['m_index'], sub_df['stock'], 1)[0])

        # Assign the beta column of the DataFrame to the betas array
        self.data['beta'] = betas
        self.data['sharpe_ratio'] = sr

    def add_stlouis_data(self):
        """Retrieve info for STLFSI and add it to the dataframe."""
        stlfsi = endpoints['stlfsi']
        url = stlfsi['base_url']
        params = stlfsi['params']
        params[''] = get_str_date()
        stlfsi_data = get_api_data(url, params, 'data/stlfsi.csv')
        self.data = self.data.join(stlfsi_data, how='left')
        self.data['STLFSI'] = self.data['STLFSI'].fillna(method='ffill')
        if isnull(self.data.ix[0]['STLFSI']):
            for i, v in self.data.iterrows():
                if isnull(v['STLFSI']):
                    continue
                try:
                    self.data.ix[0]['STLFSI'] = stlfsi_data.ix[i - dt.timedelta(weeks=1)]
                    break
                except Exception:
                    self.data['STLFSI'] = self.data['STLFSI'].fillna(method='bfill')
                    break
            self.data['STLFSI'] = self.data['STLFSI'].fillna(method='ffill')

    def fill_dataset(self):
        """Fill the dataset calling the various methods."""
        rm, rstd = self.get_rolling_stats()

        self.add_rolling_mean(rm)
        self.add_bollinger_bands(rstd)
        self.add_spy_info()
        self.add_beta_and_sharpe()
        self.add_stlouis_data()

    def get_subsets(self):
        """Return copies of the data with labels for looking n_days ahead."""
        if self.begin_date is not None and self.end_date is not None:
            iv = get_timestamp_from_date(self.end_date) - get_timestamp_from_date(self.begin_date)
            fv = iv / 86400000 + 1
            self.n_days = fv
        X = self.data.copy().ix[:self.begin_date, :]
        X = X.fillna(method='bfill')
        y = self.data.copy().ix[:self.begin_date][self.symb]
        x_pred = X.ix[-(self.n_days):, :]
        init_val = self.original_data.ix[0][self.symb]
        print X.shape, y.shape, x_pred.shape
        return X, y, x_pred, init_val

    def get_split_data(self):
        """Return train and test split data."""
        X, y, _, _ = self.get_subsets()
        return train_test_split(X, y, test_size=0.3, random_state=42)
