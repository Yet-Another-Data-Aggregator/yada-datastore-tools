"""
YADA datastore tools used to quickly moderate and reset data in the datastore during development, as well as simulate functioning hvac data logging.
"""
import os.path
from os import path
import firestore

if not path.exists('./scripts/ServiceAccountKey.json'):
    print("Firestore secret access key is required to use these utilities. Save this file to `scripts/ServiceAccountKey.json`. Make sure this key is NOT committed to this public repository")
    quit()

userInput = ""
acceptedInput = ["help", "end"] + firestore.availableQueries

while userInput != "end":
    if userInput not in acceptedInput:
        print("available commands:")
        for command in acceptedInput:
            print("\t", command)
    elif userInput == "help":
        for command in acceptedInput:
            print("\t", command)
    else:
        getattr(firestore, userInput)()
        
    userInput = input("$ ")