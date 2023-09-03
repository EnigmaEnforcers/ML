import firebase_admin
from firebase_admin import credentials, firestore
import time
from manager import img_downloader
from main import model


firCredentials = credentials.Certificate('serviceAccountKey.json')
firApp = firebase_admin.initialize_app (firCredentials)

# Get access to Firestore
db = firestore.client()
print('Connection initialized')


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['image'])
        name = doc.id
        img_downloader(name, image_url, True)
        model(name)


col_ref = db.collection('found')
doc_watch = col_ref.on_snapshot(on_snapshot)

# Keep the app running
while True:
    time.sleep(1)
