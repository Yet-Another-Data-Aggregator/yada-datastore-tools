import os, json 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
json = json.load(open('./scripts/ServiceAccountKey.json'))
cred = credentials.Certificate(json)
app = firebase_admin.initialize_app(cred)

db = firestore.client()