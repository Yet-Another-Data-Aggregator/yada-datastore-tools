import os, json 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

# Use the application default credentials
json = json.load(open('./scripts/ServiceAccountKey.json'))
cred = credentials.Certificate(json)
app = firebase_admin.initialize_app(cred)

db = firestore.client()

# queries
availableQueries = ['resetCollections', 'registerAdminEmail']
collections = ['EquipmentProfiles', 'Sites', 'Users']

def resetCollections():
  print("this function is temporarily disabled to prevent accidental data loss")
  return
  return
  # Deletes every document within the recorded collections
  for collection in collections:
    for doc in db.collection(collection).stream():
      db.collection(collection).document(doc.id).delete()

  # creates documents according to the local 'copy'


def registerAdminEmail():
  emailAddress = input("emailAddress: ")
  phoneNumber = input("phoneNumber: ")
  userPassword = input("password: ")
  userName = input("username: ")
  user = auth.create_user(
      email=emailAddress,
      email_verified=False,
      password=userPassword,
      display_name=userName,
      disabled=False)
  print('Sucessfully created new user: {0}'.format(user.uid))
  # todo: create User Document
  doc = {
    u'email': emailAddress,
    u'phoneNumber': phoneNumber,
    u'userGroup': 'owner'
  }
  db.collection('Users').document(user.uid).set(doc)