"""Module that runs the application."""
from flask import Flask, request, jsonify, render_template
from controllers.stock import Stock
from controllers.model import Model

app = Flask(__name__)

model = None


@app.route('/', methods=['GET'])
def index():
    """Index of the application."""
    return render_template('index.html'), 200


@app.route('/train/<symb>', methods=['GET', 'POST'])
def train_model(symb):
    """Train a model for the given date range and ticker symbols."""
    print(request)
    s = Stock(str(symb))
    x_tr, x_t, y_tr, y_t = s.get_split_data()
    model = Model()
    model.train(x_tr, y_tr)
    return jsonify(str(model.predict(x_t))), 200


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Make predictions for the given date range and ticker symbols."""


if __name__ == '__main__':
    """Main method."""
    app.run(host='127.0.0.1', port=5001)
