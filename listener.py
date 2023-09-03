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


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['imgUrl'])
        name = doc.id
        img_downloader(name, image_url, True)
        asyncio.run(get_imgs())
        matched = model(name)
        if not matched:
            print("No match found")
        else:
            print(name + 'looks similar to' + matched)
        file = 'Found_images/' + name + '.jpg'
        #img_deleter(file)


found_col_ref = db.collection('foundChild')
doc_watch = found_col_ref.on_snapshot(on_snapshot)


async def get_imgs():
    print("Downloading recent uploads")
    docs = lost_col_ref.get()
    for doc in docs:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['imgUrl'])
        name = doc.id
        img_downloader(name, image_url, False)


async def delete_img(filename):
    s = filename.split('/')
    key = s[-1].split('.')
    print(key[0])
    #dbref.child(key[0]).remove()


# Keep the app running
while True:
    time.sleep(1)
