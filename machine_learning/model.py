from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

from pickle4 import pickle
NB_file = 'models/GaussianNB.sav'
RF_file = 'models/Random-Forest.sav'
SVM_file = 'models/svm.sav'

def model_nb(X_train, X_test, y_train, y_test):
    # Membuat model Naive Bayes terhadap Training set
    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    pickle.dump(model, open(NB_file, 'wb'))

def model_rf(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(n_estimators= 100, random_state=0)
    model.fit(X_train,y_train)
    pickle.dump(model, open(RF_file, 'wb'))

def model_svm(X_train, X_test, y_train, y_test):
    model = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X_train, y_train)
    pickle.dump(model, open(SVM_file, 'wb'))

def predict(array, algoritm):
    filename = ''
    if algoritm == 'nb':
        filename = NB_file
    elif algoritm == 'rf':
        filename = RF_file
    elif algoritm == 'svm':
        filename = SVM_file


    # load model
    loaded_model = pickle.load(open(filename, 'rb'))
    testing_pred = loaded_model.predict([array])

    return testing_pred

