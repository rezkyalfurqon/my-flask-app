import json
import datetime
from multiprocessing import dummy
from flask import Flask, request
from flask_cors import CORS
from antares_http import antares

# my module
from machine_learning.training import training
from machine_learning.model import model_nb, model_rf, model_svm, predict
from dummy_sensor import get_data_dummy   
from database.crud import get_data, add_data
from firebase import firebase_create

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
    return "Already Trained All Algorithm."

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
        result = response['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
        res = json.loads(result)

        sensor10 = res['Sensor10']
        dummy_data = get_data_dummy(sensor10)

        convert_data = []
        for data in dummy_data:
            level = 0
            if dummy_data[data] > 0 and dummy_data[data] < 90:
                level = 1
            elif dummy_data[data] >= 90 :
                level = 2
            
            dummy_data[data] = level
            convert_data.append(level)


        kondisi_nb = int(predict(convert_data, 'nb'))
        kondisi_rf = int(predict(convert_data, 'rf'))
        kondisi_svm = int(predict(convert_data, 'svm'))

        local_time = str(datetime.datetime.now().strftime("%H %M %S"))

        antares_data = {
            "dummy_data": dummy_data,
            "convert_data": convert_data,
            "status": {
                "naive_bayes": kondisi_nb,
                "random_forest": kondisi_rf,
                "support_vector_machine": kondisi_svm
            },
            "time": local_time
        }

        antares.send(antares_data, projectName, deviceName)


    finally:
        firebase_create(antares_data, 'data')
        return 'ack'

# route to get all data from sqlite
@app.route('/get_db', methods=['GET'])
def get_db():
    res = get_data()

    return res

@app.route('/tes', methods=['GET'])
def tes():
    return str(datetime.datetime.now().strftime("%H"))

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = training()
    app.run(host="0.0.0.0", port=5000, debug=True)