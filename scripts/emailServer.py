import os, json, time, smtplib, threading
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
        emailMessages.append(msg)
    
    return emailMessages

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
            time.sleep(5.0)

if __name__ == "__main__":
    sender = threading.Thread(target=sendMail)
    print("Starting sender thread...")
    sender.start()