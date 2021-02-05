import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from getpass import getpass

# Use the application default credentials
jsonKey = json.load(open('./scripts/ServiceAccountKey.json'))
cred = credentials.Certificate(jsonKey)
app = firebase_admin.initialize_app(cred)

db = firestore.client()

# queries
availableQueries = ['resetCollections', 'registerUser', 'createCollections']

# Collections
collections = ['ChannelTemplates', 'Config', 'Loggers', 'Sites', 'Users']

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
  userName = input("Username: ")
  userPassword = getpass("Password: ")
  emailAddress = input("Email address: ")
  phoneNumber = input("Phone number: ")
  userRights = input("User group ([O]Owner, [A]Admin, [P]Power, [U]User):  ")
  while userRights not in ['O', 'o', 'A', 'a', 'P', 'p', 'U', 'u']:
    userRights = input("User group ([O]Owner, [A]Admin, [P]Power, [U]User):  ")

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

  print('Sucessfully created new user with ID: {0}'.format(user.uid))
  
  doc = {
      u'email': emailAddress,
      u'phoneNumber': phoneNumber,
      u'userGroup': userRights,
      u'defaults': True
  }

  db.collection('Users').document(user.uid).set(doc)

# Function to create database collections with default admin account
# NOTE: all collections except Config and Users are created with a document stub that contains only one field,
#       since empty documents are automatically removed by Firestore
def createCollections():
    doc = {u'name': ""}

    for c in collections:
        if c == 'Config':
            print("CONFIGURATION")
            # Get user input for config fields
            orgName = input("Organization name: ")
            ownerEmail = input("Owner's email address: ")
            defaultPass = getpass("Default user password: ")
            while len(defaultPass) < 6:
                print("Default password must be at least 6 characters!")
                defaultPass = input("Default user password: ")

            # Create dict object based on input
            data = {
                u'defaultUserPassword': defaultPass,
                u'orgName': orgName,
                u'ownerEmail': ownerEmail
            }

            # Add dict to collection
            db.collection(c).document(u'config').set(data)

            # Write dict to file
            with open('config.json', 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)

        elif c == 'Users':
            print("DATABASE OWNER")
            registerUser()
        else:
            db.collection(c).document(u'stub').set(doc) # Create document
            db.collection(c).document(u'stub').delete() # Remove it from collection

    print("Successfully created collections. To add additional users, run the registerUser function.")
    print("To set up the database again, run the resetCollections function and then the createCollections function.")