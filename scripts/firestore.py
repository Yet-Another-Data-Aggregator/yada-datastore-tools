import os, json 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
json = json.load(open('./scripts/ServiceAccountKey.json'))
cred = credentials.Certificate(json)
app = firebase_admin.initialize_app(cred)

db = firestore.client()


# queries
availableQueries = ['resetCollections']
collections = ['EquipmentProfiles', 'Sites', 'Users']

def resetCollections():
  # Deletes every document within the recorded collections
  for collection in collections:
    for doc in db.collection(collection).stream():
      db.collection(collection).document(doc.id).delete()

  # creates documents according to the local 'copy'