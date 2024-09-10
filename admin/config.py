import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init():
    KEY = credentials.Certificate('./cereal-64ada-firebase-adminsdk-mksnj-b1c782e878.json')

    firebase_admin.initialize_app(KEY,{
        'projectId': 'cereal-64ada'
    })

    return firestore.client()
