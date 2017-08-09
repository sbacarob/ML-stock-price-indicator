# Udacity-Capstone-Project
Predicting stock prices

# To run the project:

First you will need to install the dependencies in case you don't have them. You can do this by running:

`pip install -r requirements.txt`

## Start the server:

cd into the root directory and run:

`python application.py`

then you have two choices to use the application. By using the application routes, or by using the GUI on the web application.

## Using the application routes:

### Train a model on a stock:

You can train a model to make predictions for a stock by simply calling:

`GET http://localhost:5001/train/<ticker>`

If for example you wanted to train a model for the Google stock, you would call:

`GET http://localhost:5001/train/GOOG`

This will train a model on the Google stock, to predict for the next 7 days. However you can specify dates for training, or a number of days ahead to train.

### parameters:

```
pfrom: date in the format yyyy-mm-dd. Must go along with the puntil parameter
puntil: date in the format yyyy-mm-dd. Must go along with the pfrom parameter
ndays: days ahead from now to predict for. Must go alone.
```
#### Example calls: 

`GET http://localhost:5001/train/GOOG?ndays=10`

Will train a model to predict for the next ten days

`GET http://localhost:5001/train/GOOG?pfrom=2012-02-02&puntil=2012-02-09`

Will train a model to make predictions for the week from Feb 2, 2012 to Feb 9, 2012.

### Response:

When you call any of these routes, you will get back a key in the format:
`<ticker>_<days_ahead>_<begin_date>_<end_date>`

#### Examples:

`GET http://localhost:5001/train/goog`

Response:
`{"key": "goog_7_*_*"}`

`GET http://localhost:5001/train/goog?pfrom=2012-02-02&puntil=2012-02-09`

Response:
`{"key": "goog_7_2012-02-02_2012-02-09"}`

### Getting your results:

To get the prediction results, you should call the route `/predict` with the key that came as a response to your previous requests. Like this:

`GET http://localhost:5001/predict?key=goog_7_*_*`

And you would then get back a result like this:

```json
[
  930.4221, 
  930.4581000000002, 
  930.3882000000001, 
  925.3549000000003, 
  927.3287, 
  929.2324, 
  927.2102000000002
]
```

## Using the GUI:

In order to use the GUI, you just have to open your browser and go to `http://localhost:5001`

You should see something like this:

![Screenshot](https://github.com/sbacarob/Udacity-Capstone-Project/blob/master/docs/img/screenshot.png)

Here you can use the form to search for companies' symbols. Select one from the dropdown list and then specify if you want to predict for a given number of days or a date range. Specify the number of days or the date range and click on the button. A panel will be added to the right, displaying the stock price along with the predicted data.
