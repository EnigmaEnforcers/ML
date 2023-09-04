import firebase_admin
from firebase_admin import credentials, firestore
import time
from manager import *
from main import model
import asyncio

firCredentials = credentials.Certificate('serviceAccountKey.json')
firApp = firebase_admin.initialize_app(firCredentials)

# Get access to Firestore
db = firestore.client()
print('Connection initialized')
lost_col_ref = db.collection('lostChild')
found_col_ref = db.collection('foundChild')
matched_col_ref = db.collection('matchedChildren')


def on_snapshot(doc_snapshot, changes, read_time):
    asyncio.run(get_imgs())
    for doc in doc_snapshot:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['imgUrl'])
        name = doc.id
        img_downloader(name, image_url, True)
        matched = model(name)
        if not matched:
            print("No match found")
        else:
            print(name + 'looks similar to' + matched)
            lostd = lost_col_ref.document(matched).get()
            lost_dict = lostd.to_dict()
            foundd = found_col_ref.document(name).get()
            found_dict = foundd.to_dict()
            new = found_dict.update(lost_dict)
            matched_col_ref.add(new)
            lost_col_ref.document(matched).delete()
            lfile = 'Training_images' + matched + '.jpg'
            img_deleter(lfile)
        found_col_ref.document(name).delete()
        ffile = 'Found_images/' + name + '.jpg'
        img_deleter(ffile)

doc_watch = found_col_ref.on_snapshot(on_snapshot)


async def get_imgs():
    print("Downloading recent uploads")
    docs = lost_col_ref.get()
    for doc in docs:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['imgUrl'])
        name = doc.id
        img_downloader(name, image_url, False)

# Keep the app running
while True:
    time.sleep(1)
