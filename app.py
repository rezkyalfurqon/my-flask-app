from unittest import result
from flask import Flask, jsonify
from flask import request
import json
from machine_learning.training import training
from machine_learning.model import run_model, predict
import numpy as np

from antares_http import antares

projectName = 'cobamqtt'
deviceName = 'coba'

antares.setDebug(True)
antares.setAccessKey('2eca1e61d429ec86:8cb1472de9987502')

app = Flask('app')

# @app.route("/", methods=['POST'])
# def hello_world():
#     response = json.loads(request.data)
#     arrayStr = response['array'].split(',')
#     arrayInt = list(map(int, arrayStr))
#     result = run_model(X_train, X_test, y_train, y_test, arrayInt)

#     return str(result)

@app.route("/train/naive-bayes")
def train_nb():
    result = run_model(X_train, X_test, y_train, y_test)
    return "Already Trained using Naive Bayess Algorithm."

@app.route("/")
def root():
    return "<p>Hello, World!</p>"

@app.route("/get-updates")
def get_updates():
    result = antares.getAll(projectName, deviceName, limit=120)
    all_data = {
        'Sensor1' : [], 
        'Sensor2' : [], 
        'Sensor3' : [],
        'Sensor4' : [], 
        'Sensor5' : [], 
        'Sensor6' : [],
        'Sensor7' : [], 
        'Sensor8' : [], 
        'Sensor9' : [],
        'Sensor10' : [],
    }

    dates = list(filter(lambda x: 'Sensor1' in x.keys(), result))
    # return dates
    for data in result:
        sensor_key = list(data['content'].keys())[0]
        value = data['content'][sensor_key]
        level = 0

        # convert level
        if value > 0 and value < 90:
            level = 1
        elif value > 89 :
            level = 2

        all_data[sensor_key].append(level)
    
    # 0 : 0
    # 1 : 1 - 89
    # 2 : > 89

    result_set = []
    for i in range(10):
        sensors = []
        # baru sensor 1-9
        for j in range(9):
            sensors.append(all_data['Sensor'+str(int(j+1))][i])
        # dummy sensor10
        sensors.append(1)

        print("set-ke:",i+1,sensors)
        predicted = int(predict(sensors))
        # result_set['Sensors'].append(sensors)
        # result_set['Status'].append(predicted)
        result_set.append({
            'Sensors' : sensors,
            'Status' : predicted
        })
    return jsonify(data=result_set)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = training()
    app.run(host="0.0.0.0", port=5000, use_reloader=True)
