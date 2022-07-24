from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

from pickle4 import pickle
filename = 'models/GaussianNB.sav'

def run_model(X_train, X_test, y_train, y_test):
    # Membuat model Naive Bayes terhadap Training set
    model = GaussianNB()
    model.fit(X_train, y_train)

    pickle.dump(model, open(filename, 'wb'))



def predict(array):
    # load model
    loaded_model = pickle.load(open(filename, 'rb'))
    testing_pred = loaded_model.predict([array])

    return testing_pred

