import os
import json
import time
import smtplib
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from email.message import EmailMessage

# Use the application default credentials
jsonKey = json.load(open('ServiceAccountKey.json'))
cred = credentials.Certificate(jsonKey)
app = firebase_admin.initialize_app(cred)

db = firestore.client()


def getAdminAddresses():
    docs = db.collection("Users").where(
        "userGroup", "in", ["Owner", "Admin"]
    ).where(
        "emailNotifications", "==", True
    ).stream()
    return [doc.to_dict()["email"] for doc in docs]


def getEmails():
    docs = db.collection("Emails").stream()
    emails = [doc.to_dict() for doc in docs]

    emailMessages = []
    for e in emails:
        msg = EmailMessage()
        msg.set_content(e["message"])
        msg["Subject"] = e["subject"]
        msg["From"] = e["email"]
        emailMessages.append(msg)

    return emailMessages


def getFaultEmails():
    docs = db.collection("Notifications").stream()
    faults = [doc.to_dict() for doc in docs]
    emails = []
    for fault in faults:
        loggerId = fault['logger']
        message = fault['message']
        # get siteID and equipment name
        loggerDoc = db.collection(u'Loggers').document(
            loggerId).get().to_dict()
        siteId = loggerDoc['site']
        siteDoc = db.collection(u'Sites').document(siteId).get().to_dict()
        equipName = ''
        for unit in siteDoc['equipmentUnits']:
            if (loggerId in unit['loggers']):
                equipName = unit['name']

        # iterate over user documents
        users = [doc.to_dict() for doc in db.collection("Users").stream()]
        for user in users:
            if (('equipmentNotifications' in user)):
                if (siteId in user['equipmentNotifications']):
                    subscribed = user['equipmentNotifications'][siteId][equipName]
                    notificationsOn = ('emailNotifications' in user and user['emailNotifications']) or ('emailNotifications' not in user)
                    if subscribed and notificationsOn:
                        # generate email
                        emailRecipient = user['email']
                        emailSubject = f"Fault detected on {equipName}"
                        emailContent = message

                        msg = EmailMessage()
                        msg.set_content(emailContent)
                        msg["Subject"] = emailSubject
                        msg["To"] = emailRecipient
                        emails.append(msg)

    return emails


def deleteFaults():
    docs = db.collection('Notifications').stream()
    for doc in docs:
        db.collection("Notifications").document(doc.id).delete()


def deleteEmails():
    docs = db.collection("Emails").stream()
    for doc in docs:
        db.collection("Emails").document(doc.id).delete()


def sendMail():
    EMAIL = "YADA.Sender@gmail.com"
    PASS = "HLt8AJpfNgm8Jvn"
    adminAddresses = "YADA.Sender@gmail.com, " + ", ".join(getAdminAddresses())

    while True:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10.0) as server:
            server.ehlo()
            server.login(EMAIL, PASS)

            emails = getEmails()
            for e in emails:
                server.sendmail(e["From"], adminAddresses, e.as_string())
                print(f'Sent message from {e.get("From")}.')
            deleteEmails()

            notifications = getFaultEmails()
            for n in notifications:
                server.sendmail(EMAIL, [n["To"], EMAIL], n.as_string())
                print(f'Sent message to {n["To"]}.')
            deleteFaults()

            time.sleep(5.0)


if __name__ == "__main__":
    sender = threading.Thread(target=sendMail)
    print("Starting sender thread...")
    sender.start()
