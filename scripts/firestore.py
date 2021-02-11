import os
import json
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
availableQueries = ['resetCollections', 'registerUser', 'generateData', 'generateFault']
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
                    u'equipment': None,  # TODO: fix this
                    u'ip': 'ip addr',
                    u'mac': 'mac address',
                    u'notes': 'any notes for this logger',
                    u'site': 'siteID',  # TODO: fix this
                    u'status': True,
                    u'uptime': None,
                    u'data': [
                        # TODO: add data
                    ]
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
                        # TODO: add users
                    },
                    u'equipmentUnits': {
                        u'inside top left hvac': {  # TODO: fix this
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
    selectedLoggers = []
    invalidInput = True

    # get list of available sites
    sites = getSites()
    # TODO: while active, generate data for every logger and push to datastore. This relies on the logger profiles to generate valid data

def generateFault():
    selectedLoggers = []
    userInput = ''

    # list of available sites
    sites = getSites()
    while (not userInput.isdecimal()) or int(userInput) not in range(len(sites)):
        index = 0
        for site in sites:
            print(f'[{index}] {site.to_dict()["name"]}')
            index += 1
        userInput = input('Select site to generate fault: ')
    
    site = sites[int(userInput)]
    # get logger channels for the loggers and generate faults


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


# ------

def getSites():
    sites = []
    for doc in db.collection('Sites').stream():
        sites.append(doc)
    return sites
