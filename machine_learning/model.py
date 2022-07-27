from sklearn.naive_bayes import GaussianNB

# from pickle4 import pickle
# filename = 'models/GaussianNB.sav'

model = GaussianNB()
def run_model(X_train, X_test, y_train, y_test):
    # Membuat model Naive Bayes terhadap Training set
    model.fit(X_train, y_train)

    # pickle.dump(model, open(filename, 'wb'))



def predict(array):
    # load model
    # loaded_model = pickle.load(open(filename, 'rb'))
    testing_pred = model.predict([array])

    return testing_pred

