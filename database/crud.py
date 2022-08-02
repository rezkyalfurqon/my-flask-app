import sqlite3 as sql

def get_data():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from mitigasi")
    data = cur.fetchall()

    response = []
    for d in data:
        res = {}
        res['sensor1'] = d['sensor1']
        res['sensor2'] = d['sensor2']
        res['sensor3'] = d['sensor3']
        res['sensor4'] = d['sensor4']
        res['sensor5'] = d['sensor5']
        res['sensor6'] = d['sensor6']
        res['sensor7'] = d['sensor7']
        res['sensor8'] = d['sensor8']
        res['sensor9'] = d['sensor9']
        res['sensor10'] = d['sensor10']
        res['kondisi_nb'] = d['kondisi_nb']
        res['kondisi_rf'] = d['kondisi_rf']
        res['kondisi_svm'] = d['kondisi_svm']
        res['time'] = d['time']

        response.append(res)
    
    return {'data': response[0]}


def add_data(data):
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute("insert into mitigasi(sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9, sensor10, kondisi_nb, kondisi_rf, kondisi_svm, time) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['Sensor1'], data['Sensor2'], data['Sensor3'], data['Sensor4'], data['Sensor5'], data['Sensor6'], data['Sensor7'], data['Sensor8'], data['Sensor9'], data['Sensor10'], data['kondisi_nb'], data['kondisi_rf'], data['kondisi_svm'], data['time']))
    con.commit()

    return {'message': 'success'}