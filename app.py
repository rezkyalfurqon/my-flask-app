import json
import datetime
from flask import Flask, request
from flask_cors import CORS
from antares_http import antares
from firebase import firebase_create

# my module
from machine_learning.training import training
from machine_learning.model import model_nb, model_rf, model_svm, predict
from dummy_sensor import get_data_dummy   

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
        # result = response['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
        result = response['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
        res = json.loads(result)

        sensor10 = res['Sensor10']
        dummy_data = get_data_dummy(sensor10)
        convert_data = {}

        predict_data = []
        for data in dummy_data:
            level = 0
            if dummy_data[data] > 0 and dummy_data[data] < 90:
                level = 1
            elif dummy_data[data] >= 90 :
                level = 2
            
            convert_data[data] = level
            predict_data.append(level)


        hasil_nb = int(predict(predict_data, 'nb'))
        hasil_rf = int(predict(predict_data, 'rf'))
        hasil_svm = int(predict(predict_data, 'svm'))

        local_time = str(datetime.datetime.now().strftime("%H:%M:%S"))

        antares_data = {
            "dummy_data": dummy_data,
            "convert_data": convert_data,
            "local_time": local_time,
            "status": {
                "naive_bayes": hasil_nb,
                "random_forest": hasil_rf,
                "support_vector_machine": hasil_svm
            }
        }

        antares.send(antares_data, projectName, deviceName)


        # add_data(allData)
        firebase_create(antares_data, 'antares')
        firebase_create({
                "naive_bayes": hasil_nb,
                "random_forest": hasil_rf,
                "support_vector_machine": hasil_svm,
                "local_time": local_time,
            }, 'status')
    finally:
        return 'ack'

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = training()
    app.run(host="0.0.0.0", port=5000, debug=True)