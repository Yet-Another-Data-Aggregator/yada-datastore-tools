import os, json, time, smtplib
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
    docs = db.collection("Users").where("userGroup", "in", ["Owner", "Admin"]).stream()

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
        emailMessages.append(e)
    
    return emailMessages

with smtplib.SMTP("smtp.mailtrap.io", 465) as server:
    server.login("7ef8ab7208d17b", "d16d657eeea76f")
    adminAddresses = ", ".join(getAdminAddresses())
    for e in getEmails():
        print(e)
        server.sendmail(e["From"], adminAddresses, e.as_string())

print("Sent.")