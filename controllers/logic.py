"""Handle the general logic required for the route responses."""
from stock import Stock
from model import Model

models = {}


def train(symb, n_days, begin_date, end_date):
    """Train a model given a symbol and training dates."""
    key = get_key(symb, n_days, begin_date, end_date)
    models[key] = {}
    current_model = models[key]
    current_model = {
        'status': 102,
        'model': None
    }
    try:
        s = Stock(str(symb), n_days, begin_date=begin_date, end_date=end_date)
        X, y, x_pred, init_val = s.get_subsets()
        model = Model()
        current_model['model'] = model
        current_model['init_val'] = init_val
        current_model['predict_data'] = x_pred
        models[key] = current_model
        model.train(X, y)
    except Exception as e:
        current_model['status'] = 500
        current_model['error'] = e.message
        models[key] = current_model


def predict(key):
    """Make predictions for a model that has already been trained."""
    if key not in models:
        return "Model hasn't been trained", 400
    model = models[key]
    print models[key]
    if model['model'] is None:
        return "Model not available", model['status']
    try:
        predictions = model['model'].predict(model['predict_data'])
        print predictions[0]
        res = [k * model['init_val'] for k in predictions.tolist()]
        print res[0]
        return res, 200
    except Exception as e:
        return e.message, 500


def get_key(symb, n_days, begin_date, end_date):
    """Generate the key to store the model in the models dict."""
    symb = symb.lower()
    if begin_date == '':
        begin_date = '*'
    if end_date == '':
        end_date = '*'
    if n_days == '':
        n_days = '7'
    return '%s_%s_%s_%s' % (symb, n_days, begin_date, end_date)


def get_key_status(key):
    """Get the response status code to give based on whether the model exists."""
    return 302 if key in models else 200
