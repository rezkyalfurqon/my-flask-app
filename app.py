from flask import Flask, jsonify
from flask import request
import json
from machine_learning.training import training
from machine_learning.model import run_model, predict
from dummy_sensor import sendData   
import numpy as np

from antares_http import antares

import sqlite3

projectName = 'cobamqtt'
deviceName = 'coba2'

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
    result = antares.get(projectName, deviceName)
    # all_data = {
    #     'Sensor1' : [], 
    #     'Sensor2' : [], 
    #     'Sensor3' : [],
    #     'Sensor4' : [], 
    #     'Sensor5' : [], 
    #     'Sensor6' : [],
    #     'Sensor7' : [], 
    #     'Sensor8' : [], 
    #     'Sensor9' : [],
    #     'Sensor10' : [],
    # }

    # dates = list(filter(lambda x: 'Sensor1' in x.keys(), result))
    # # return dates
    # for data in result:
    #     sensor_key = list(data['content'].keys())[0]
    #     value = data['content'][sensor_key]
    #     level = 0

    #     # convert level
    #     if value > 0 and value < 90:
    #         level = 1
    #     elif value > 89 :
    #         level = 2

    #     all_data[sensor_key].append(level)
    
    # # 0 : 0
    # # 1 : 1 - 89
    # # 2 : > 89

    # result_set = []
    # for i in range(10):
    #     sensors = []
    #     # baru sensor 1-9
    #     for j in range(9):
    #         sensors.append(all_data['Sensor'+str(int(j+1))][i])
    #     # dummy sensor10
    #     sensors.append(1)

    #     print("set-ke:",i+1,sensors)
    #     predicted = int(predict(sensors))
    #     # result_set['Sensors'].append(sensors)
    #     # result_set['Status'].append(predicted)
    #     result_set.append({
    #         'Sensors' : sensors,
    #         'Status' : predicted
    #     })
    # return jsonify(data=result_set)
    return result

@app.route('/monitor', methods=['POST'])
def monitor():
    response = json.loads(request.data)
    # result = response['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
    result = response['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
    
    res = result.replace("{", "")
    res = res.replace("}", "")
    res = res.split(':')
    res = res[len(res) - 1]

    allData = sendData(res)

    arrForPredict = []
    for data in allData:
        arrForPredict.append(allData[data])
        # print(allData[data])

    hasil = int(predict(arrForPredict))
    print('hasil = ' + str(hasil))

    # query_db("INSERT INTO mitigasi_gempa (sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9, sensor10, kondisi)", (allData[0], allData[1], allData[2], allData[3], allData[4], allData[5], allData[6], allData[7], allData[8], allData[9], hasil))

    # params = [allData[0], allData[1], allData[2], allData[3], allData[4], allData[5], allData[6], allData[7], allData[8], allData[9], hasil]
    # insertToDB(params)
    
    # insertToDB(list(allData.values()))
    try: 
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO mitigasi_gempa (sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9, sensor10, kondisi) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(list(allData.values())))
            
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    
    finally:
        con.close()

    return 'ack'

# @app.route('/getDB', methods=['GET'])
# def getDataFromDB():
#     con = sqlite3.connect("database.db")
#     con.row_factory = sqlite3.Row
    
#     cur = con.cursor()
#     cur.execute("SELECT * FROM mitigasi_gempa")
    
#     rows = cur.fetchall();
#     return rows



# if __name__ == "__main__":
#     X_train, X_test, y_train, y_test = training()
#     app.run(host="0.0.0.0", port=9000, use_reloader=True)
