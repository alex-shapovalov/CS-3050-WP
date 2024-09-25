import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init():
    cred = credentials.Certificate("../admin/cereal-64ada-firebase-adminsdk-mksnj-f3e226c1aa.json")
    firebase_admin.initialize_app(cred)

    return firestore.client()
