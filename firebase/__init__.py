import uuid
from firebase_admin import initialize_app, firestore
from firebase_admin import credentials
from flask import jsonify

cred = credentials.Certificate("firebase/firebase-key.json")
initialize_app(cred)
db = firestore.client()

def firebase_create(data, collection):
    data_ref = db.collection(collection)
    try:
        id = uuid.uuid4()
        data_ref.document(id.hex).set(data)

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False}), 400
