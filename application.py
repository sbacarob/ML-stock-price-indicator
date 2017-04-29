"""Module that runs the application."""
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Index of the application."""
    return render_template('index.html'), 200


@app.route('/train', methods=['GET', 'POST'])
def train_model():
    """Train a model for the given date range and ticker symbols."""


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Make predictions for the given date range and ticker symbols."""


if __name__ == '__main__':
    """Main method."""
    app.run(host='127.0.0.1', port=5001)
