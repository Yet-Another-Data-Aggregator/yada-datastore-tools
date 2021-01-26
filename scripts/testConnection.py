import firestore

def testing(value):
    db.collection(u'testCollection').document(u'test').set({
        u'something': u'testing'
    })