from crypt import methods
import email
import json
import datetime
from re import A
from flask import Flask, request, jsonify
from flask_cors import CORS
from antares_http import antares

# my module
from firebase import db_create, db_push, db_get, db_push_child, firestore_add, firestore_get
from machine_learning.training import training
from machine_learning.model import model_nb, model_rf, model_svm, predict
from dummy_sensor import get_data_dummy   

projectName = 'MitigasiGempa'
deviceName = 'KondisiAkhir'

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
    return "<p>Server is Already Running</p>"

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

@app.route('/get_kondisi/<algoritm>', methods=['GET'])
def get_kondisi(algoritm):

    data = db_get('latestReport')

    return jsonify({"data": data[algoritm], "message": "success"}), 200

@app.route('/get_current_algoritm', methods=['GET'])
def get_current_algoritm():

    current_algoritm = db_get('currentAlgoritm')

    return jsonify({"data": current_algoritm, "message": "success"}), 200

@app.route('/set_current_algoritm', methods=['POST'])
def set_current_algoritm():
    data = request.get_json()
    print(data)

    res = db_create(data['algoritm'], 'currentAlgoritm')

    if res:
        return jsonify({"message": "succes"}), 200
    else:
        return jsonify({"message": "faild"}), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data['name']
    telp = data['telp']
    email = data['email']
    password = data['password']

    res = firestore_add('users', email, {
        "name": name,
        "email": email,
        "telp": telp,
        "password": password
    })

    if res :
        return jsonify({"message": "success"}), 201
    else:
        return jsonify({"message": "faild"}), 400
        

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    res = firestore_get('users', email)

    if res and res['password'] == password:
        del res['password']
        return jsonify({"data": res, "message": 'success'}), 200

    else:
        return jsonify({"data": {}, "message": 'faild'}), 400

@app.route('/get_profile', methods=['POST'])
def get_profile():
    data = request.get_json()

    email = data['email']

    res = firestore_get('users', email)

    if res:
        del res['password']
        return jsonify({"data": res, "message": 'success'}), 200

    else:
        return jsonify({"data": {}, "message": 'faild'}), 400

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
            if dummy_data[data] > 0 and dummy_data[data] < 89:
                level = 1
            elif dummy_data[data] >= 89 :
                level = 2
            
            convert_data[data] = level
            predict_data.append(level)


        hasil_nb = int(predict(predict_data, 'nb'))
        hasil_rf = int(predict(predict_data, 'rf'))
        hasil_svm = int(predict(predict_data, 'svm'))

        local_time = str(datetime.datetime.now().strftime("%H:%M:%S"))
        local_date = str(datetime.datetime.now().strftime("%d %b %Y"))

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

        # push data to antares
        antares.send(antares_data, projectName, deviceName)
        
        # lastReport
        db_create({
                "NB": hasil_nb,
                "RF": hasil_rf,
                "SVM": hasil_svm,
                "local_date": local_date,
                "local_time": local_time,
            }, 'latestReport')

        # history
        history = convert_data
        history["local_time"] = local_time
        history["local_date"] = local_date

        if hasil_nb == 2:
            db_push_child(history, 'history', 'NB')
        
        if hasil_rf == 2:
            db_push_child(history, 'history', 'RF')
        
        if hasil_svm == 2:
            db_push_child(history, 'history', 'SVM')
    finally:
        return 'ack'

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = training()
    app.run(host="0.0.0.0", port=5000, debug=True)