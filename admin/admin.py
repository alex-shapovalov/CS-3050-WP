import firebase-admin
from firebase-admin import credentials
from firebase-admin import firestore

KEY = credentials.Certificate('./cereal-64ada-firebase-adminsdk-mksnj-b1c782e878.json')
firebase-admin.initialize_app(KEY,{
    'projectID': 'cereal-64ada'
}
)