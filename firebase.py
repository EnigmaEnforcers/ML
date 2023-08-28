import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests

cred = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://accenture-578fc-default-rtdb.firebaseio.com"
})

dbref = db.reference("/lost") 
lost = dbref.get()

for key, value in lost.items():
    print(value['image'])


