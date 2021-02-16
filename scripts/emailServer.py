import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import time
import threading

# Use the application default credentials
jsonKey = json.load(open('ServiceAccountKey.json'))
cred = credentials.Certificate(jsonKey)
app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    print(u'Callback received query snapshot.')
    for doc in col_snapshot:
        print(f'{doc.id}')
    callback_done.set()

col_query = db.collection(u'Emails')

# Watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)