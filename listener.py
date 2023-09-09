import firebase_admin
from firebase_admin import credentials, firestore, storage
import time
from manager import *
from main import model
import asyncio

firCredentials = credentials.Certificate('serviceAccountKey.json')
firApp = firebase_admin.initialize_app(firCredentials, {'storageBucket' : 'gs://accenture-578fc.appspot.com/lost_user_image'})

# Get access to Firestore
db = firestore.client()
print('Connection initialized')
lost_col_ref = db.collection('lostChild')
found_col_ref = db.collection('foundChild')
matched_col_ref = db.collection('matchedChildren')
bucket = storage.bucket()


def on_snapshot(doc_snapshot, changes, read_time):
    print("-----Downloading recent uploads-----")
    asyncio.run(get_imgs())
    for doc in doc_snapshot:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['imgUrl'])
        name = doc.id
        img_downloader(name, image_url, True)
        matched = model(name)
        if not matched:
            print("-----No match found-----")
        else:
            print('----- ' + name + ' looks similar to ' + matched + ' -----')
            lostd = lost_col_ref.document(matched).get()
            lost_dict = lostd.to_dict()
            foundd = found_col_ref.document(name).get()
            found_dict = foundd.to_dict()
            new = {
                'childName': lost_dict['childName'],
                'childAge': lost_dict['childAge'],
                'parentName': lost_dict['parentName'],
                'parentsContact': lost_dict['parentsContact'],
                'description': found_dict['foundChildDescription'],
                'imgUrl': found_dict['imgUrl'],
                'lostDate': lost_dict['lostDate']
            }
            matched_col_ref.add(new)
            lost_col_ref.document(matched).delete()
            lost_file = 'Training_images/' + matched + '.jpg'
            img_deleter(lost_file)
        found_col_ref.document(name).delete()
        found_file = 'Found_images/' + name + '.jpg'
        img_deleter(found_file)


doc_watch = found_col_ref.on_snapshot(on_snapshot)


async def get_imgs():
    docs = lost_col_ref.get()
    for doc in docs:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['imgUrl'])
        name = doc.id
        img_downloader(name, image_url, False)

# Keep the app running
while True:
    time.sleep(60)
    print("Waiting for changes")
