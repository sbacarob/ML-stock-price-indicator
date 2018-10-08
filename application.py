"""Module that runs the application."""
from time import sleep
from json import dumps
from threading import Thread
from controllers.logic import *
from controllers.helpers import *
from controllers.stock import Stock
from controllers.model import Model
from datetime import timedelta, datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Index of the application."""
    return render_template('index.html'), 200


@app.route('/train/<symb>', methods=['GET', 'POST'])
def train_model(symb):
    """Train a model for the given prediction date range and ticker symbols."""
    print request
    begin_date = request.args.get('pfrom', '')
    end_date = request.args.get('puntil', '')
    n_days = request.args.get('ndays', '')
    if n_days != '':
        n_days = int(n_days)
    key = get_key(symb, n_days, begin_date, end_date)
    response_status = get_key_status(key)
    t = Thread(target=train, args=(symb, n_days, begin_date, end_date))
    t.start()
    resp = dumps({'key': key})
    return resp, response_status


@app.route('/predict', methods=['GET', 'POST'])
def prediction():
    """Make predictions for the given date range and ticker symbols."""
    key = request.args.get('key', '')
    resp, status = predict(key)
    if status == 200:
        return dumps(resp), status
    return resp, status


@app.route('/hcdata', methods=['GET'])
def get_hc_ready_data():
    """Return the data for some stock in the format used by Highcharts."""
    symb = request.args.get('symb', '')
    stock = retrieve_stock_info(symb)
    list_in_hc = [[ix.value / 1000000 if type(ix) is not str else get_timestamp_from_date(ix),
                   k[symb]] for ix, k in stock.iterrows()]
    return dumps(list_in_hc), 200


@app.route('/test', methods=['GET'])
def test():
    """Test the app is running and concurrency is working."""
    t = Thread(target=some_test)
    t.start()
    return "Your request has been received. And you'll see results shortly", 200


@app.route('/tickers/<term>', methods=['GET'])
def get_tickers(term):
    """Get a list of possible symbols for a given query."""
    return dumps(get_query_related_tickers(term)), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, threaded=True)
