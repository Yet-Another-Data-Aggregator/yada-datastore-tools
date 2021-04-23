import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from getpass import getpass

# Use the application default credentials
jsonKey = json.load(open('ServiceAccountKey.json'))
cred = credentials.Certificate(jsonKey)
app = firebase_admin.initialize_app(cred)

db = firestore.client()

# queries
availableQueries = ['resetCollections', 'registerUser',
                    'generateData', 'pushSpecificData', 'createCollections']
# Collections
collections = ['ChannelTemplates', 'Config', 'Loggers', 'Sites']


def resetCollections():
    # Deletes every document within the recorded collections
    for collection in collections:
        for doc in db.collection(collection).stream():
            db.collection(collection).document(doc.id).delete()

    # creates documents according to the local 'copy'
    defaultData = {
        u'ChannelTemplates': {
            u'autoID': [{
                u'channels': {
                    u'exampleChannelName': u'/filepath/to/document'  # TODO: fix this
                },
                u'name': 'Example name for the template'
            }],
            u'specificID': {}
        },
        u'Config': {
            u'autoID': [],
            u'specificID': {
                u'config': {
                    u'defaultUserPassword': "yadaDefault",
                    u'orgName': 'organisation name',
                    u'ownerEmail': 'jorstadsd17@gcc.edu'
                }
            }
        },
        u'Loggers': {
            u'autoID': [
                {
                    u'channelTemplate': u'templateID',  # TODO: fix this
                    u'collectingData': True,
                    u'equipment': None,
                    u'ip': 'ip addr',
                    u'mac': 'mac address',
                    u'notes': 'any notes for this logger',
                    u'site': None,
                    u'status': True,
                    u'uptime': None,
                    u'data': []
                }
            ],
            u'specificID': {}
        },
        u'Sites': {
            u'autoID': [
                {
                    u'address': '200 campus drive, grove city pa, 16127',
                    u'name': 'Grove City Stem',
                    u'notes': 'Notes on the stem buiding site',
                    u'userNotifications': {
                    },
                    u'equipmentUnits': {
                        u'inside top left hvac': {
                            u'faults': [],
                            u'loggers': []
                        }
                    }
                }
            ],
            u'specificID': {},
        }
    }
    # inserts the documents specified in defaultData
    for collection in defaultData.keys():
        for docDict in defaultData[collection]['autoID']:
            createdDoc = db.collection(collection).add(docDict)
        for (docID, docDict) in defaultData[collection]['specificID'].items():
            createdDoc = db.collection(collection).document(docID).set(docDict)


def generateData():
    """
    pushes the following data to the specified logger
    """
    loggerId = ''
    data = {
        u'data': firestore.FieldValue.arrayUnion({
            
        })
    }

    db.collection('Loggers').document(loggerId).update(data)


def registerUser():
    emailAddress = input("emailAddress: ")
    phoneNumber = input("phoneNumber: ")
    userPassword = getpass("password: ")
    userName = input("username: ")
    userRights = input("user group: [O]Owner, [A]Admin, [P]Power, [U]User")
    while userRights not in ['O', 'o', 'A', 'a', 'P', 'p', 'U', 'u']:
        userRights = input(
            "user group: [O]Owner, [A]Admin, [P]Power, [U]User:  ")

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


def getSites():
    sites = []
    for doc in db.collection('Sites').stream():
        sites.append(doc)
    return sites

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
            db.collection(c).document(u'stub').set(doc)  # Create document
            # Remove it from collection
            db.collection(c).document(u'stub').delete()

    print("Successfully created collections. To add additional users, run the registerUser function.")
    print("To set up the database again, run the resetCollections function and then the createCollections function.")
