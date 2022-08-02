import json
from flask import Flask, request
from flask_cors import CORS
from antares_http import antares

# my module
from machine_learning.training import training
from machine_learning.model import model_nb, model_rf, model_svm, predict
from dummy_sensor import get_data_dummy   
from database.crud import get_data, add_data

projectName = 'cobamqtt'
deviceName = 'coba2'

antares.setDebug(True)
antares.setAccessKey('2eca1e61d429ec86:8cb1472de9987502')

app = Flask(__name__)
CORS(app)

# global variable
X_train = 0
X_test = 0
y_train = 0
y_test = 0

@app.route("/")
def root():
    return "<p>Hello, World!</p>"

# route to run model machine learning
@app.route("/train")
def train_nb():
    
    model_nb(X_train, X_test, y_train, y_test)
    model_rf(X_train, X_test, y_train, y_test)
    model_svm(X_train, X_test, y_train, y_test)
    return "Already Trained using Naive Bayess Algorithm."

# route to get latest data from antares
@app.route("/get_antares")
def get_updates():
    result = antares.get(projectName, deviceName)
    
    return result

# route to subscribe service antares
@app.route('/monitor', methods=['POST'])
async def monitor():
    try:
        response = json.loads(request.data)
        # result = response['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
        result = response['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
        res = json.loads(result)

        sensor10 = res['Sensor10']
        allData = get_data_dummy(sensor10)

        arrForPredict = []
        for data in allData:
            level = 0
            if allData[data] > 0 and allData[data] < 90:
                level = 1
            elif allData[data] >= 90 :
                level = 2
            
            allData[data] = level
            arrForPredict.append(level)


        hasil_nb = int(predict(arrForPredict, 'nb'))
        hasil_rf = int(predict(arrForPredict, 'rf'))
        hasil_svm = int(predict(arrForPredict, 'svm'))

        allData['kondisi_nb'] = hasil_nb
        allData['kondisi_rf'] = hasil_rf
        allData['kondisi_svm'] = hasil_svm

        antares.send(allData, projectName, deviceName)

        add_data(allData)
    finally:
        return 'ack'

# route to get all data from sqlite
@app.route('/get_db', methods=['GET'])
def get_db():
    res = get_data()

    return res[0]

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = training()
    app.run(host="0.0.0.0", port=5000, debug=True)