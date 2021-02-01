import os, json 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from getpass import getpass

# Use the application default credentials
json = json.load(open('./scripts/ServiceAccountKey.json'))
cred = credentials.Certificate(json)
app = firebase_admin.initialize_app(cred)

db = firestore.client()

# queries
availableQueries = ['resetCollections', 'registerUser']
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


def registerUser():
  emailAddress = input("emailAddress: ")
  phoneNumber = input("phoneNumber: ")
  userPassword = getpass("password: ")
  userName = input("username: ")
  userRights = input("user group: [O]Owner, [A]Admin, [P]Power, [U]User")
  while userRights not in ['O', 'o', 'A', 'a', 'P', 'p', 'U', 'u']:
    userRights = input("user group: [O]Owner, [A]Admin, [P]Power, [U]User:  ")

  if userRights in ['o', 'O']:
    userRights = 'Owner'
  if userRights in ['A', 'a']:
    userRights = 'Admin'
  if userRights in ['P', 'p']:
    userRights = 'Power'
  if userRights in ['U', 'u']:
    userRights == 'User'

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
    u'userGroup': userRights,
    u'defaults': True
  }
  db.collection('Users').document(user.uid).set(doc)

# Function to initialize database with default admin account
def createDB():
  pass

# New example