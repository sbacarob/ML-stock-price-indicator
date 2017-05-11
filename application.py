"""Module that runs the application."""
from controllers.stock import Stock
from controllers.model import Model
from datetime import timedelta, datetime
from flask import Flask, request, jsonify, render_template
from controllers.helpers import retrieve_stock_info, get_timestamp_from_date, get_query_related_tickers

app = Flask(__name__)

model = None

cached_models = {}


@app.route('/', methods=['GET'])
def index():
    """Index of the application."""
    return render_template('index.html'), 200


@app.route('/train/<symb>', methods=['GET', 'POST'])
def train_model(symb):
    """Train a model for the given date range and ticker symbols."""
    print(request)
    s = Stock(str(symb))
    X, y, x_pred = s.get_subsets()
    model = Model()
    model.train(X, y)
    return jsonify(str(model.predict(x_pred))), 200


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Make predictions for the given date range and ticker symbols."""


@app.route('/hcdata', methods=['GET'])
def get_hc_ready_data():
    """Return the data for some stock in the format used by Highcharts."""
    symb = request.args.get('symb', '')
    stock = retrieve_stock_info(symb)
    list_in_hc = [[ix.value / 1000000 if type(ix) is not str else get_timestamp_from_date(ix),
                   k[symb]] for ix, k in stock.iterrows()]
    return jsonify(list_in_hc), 200


@app.route('/hcpredict', methods=['GET'])
def get_hc_prediction_data():
    """Return the data for a stock and predictions for the given number of days."""
    symb = request.args.get('symb', '')
    n_days = int(request.args.get('days', ''))
    s = Stock(symb)
    stock = retrieve_stock_info(symb)
    X, y, x_pred = s.get_subsets(n_days=n_days)
    model = Model()
    model.train(X, y)
    t_a = x_pred.index[0]
    t_b = datetime.now()
    diff = t_b - t_a
    delta = int(diff.total_seconds() / 60 / 60 / 24)
    predicted_dates = [(val + timedelta(days=delta)).value / 1000000 for val in x_pred.index]
    predicted = model.predict(x_pred)
    print predicted
    pred_res = [[predicted_dates[i], k * stock.ix[0][symb]] for i, k in enumerate(predicted)]
    print pred_res
    return jsonify({'base': [[ix.value / 1000000, k[symb]] for ix,
                             k in stock.iterrows()], 'predicted': pred_res})


@app.route('/tickers/<term>', methods=['GET'])
def get_tickers(term):
    """Get a list of possible symbols for a given query."""
    return jsonify(get_query_related_tickers(term)), 200


if __name__ == '__main__':
    """Main method."""
    app.run(host='127.0.0.1', port=5001)
