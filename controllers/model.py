"""Module to store the model class."""
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor


class Model(object):

    """The model that we'll train and use to make predictions."""

    def __init__(self):
        """Create an instance of the model to make predictions."""
        self.base_clf = KNeighborsRegressor(weights='distance')
        # self.base_clf = SVR(kernel='poly', verbose=True, degree=5, max_iter=1000000)
        # self.end_clf = AdaBoostRegressor(base_estimator=self.base_clf, random_state=42)
        print "#" * 100
        print "Los cambios quedan"
        print "#" * 100
        self.end_clf = RandomForestRegressor(random_state=42, criterion='mae',
                                             n_estimators=50, min_samples_split=6)

    def train(self, X_train, y_train):
        """Train the model with the given training data and labels."""
        self.end_clf.fit(X_train, y_train)

    def predict(self, X):
        """Make predictions for the given X."""
        return self.end_clf.predict(X)
