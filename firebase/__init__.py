import uuid
from firebase_admin import initialize_app, firestore, db
from firebase_admin import credentials
from flask import jsonify

cred = credentials.Certificate("firebase/firebase-key.json")
initialize_app(cred, {'databaseURL': 'https://mitigasi-gempa-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def db_create(data, path):
    data_ref = db.reference(path)
    try:
        data_ref.set(data)

        return True
    except:
        return False

def db_push(data, path):
    data_ref = db.reference(path)
    try:
        data_ref.push(data)

        return True
    except:
        return False

def db_push_child(data, path, child):
    data_ref = db.reference(path)
    try:
        data_ref.child(child).push(data)

        return True
    except:
        return False

def db_get(path):
    data_ref = db.reference(path)

    try:
        return data_ref.get()
    except:
        return False
        
        
def firestore_add(col, doc, data):
    ref = firestore.client()

    try:
        ref.collection(col).document(doc).set(data)
        return True
    except Exception as e:
        return False

def firestore_get(col, doc):
    ref = firestore.client()

    res = ref.collection(col).document(doc).get()

    if res.exists:
        return res.to_dict()
    else:
        return False



