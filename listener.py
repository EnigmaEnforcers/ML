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
print('-----Connection initialized-----')
lost_col_ref = db.collection('lostChild')
found_col_ref = db.collection('foundChild')
matched_col_ref = db.collection('matchedChildren')
bucket = storage.bucket()
faceless = set()


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
            delete_imgs(matched, False)
        delete_imgs(name, True)


doc_watch = found_col_ref.on_snapshot(on_snapshot)


async def get_imgs():
    docs = lost_col_ref.get()
    for doc in docs:
        doc_dict = doc.to_dict()
        image_url = (doc_dict['imgUrl'])
        name = doc.id
        img_downloader(name, image_url, False)


def delete_imgs(name, found):
    if found:
        path = 'Found_images/' + name + '.jpg'
        found_col_ref.document(name).delete()
    else:
        path = 'Training_images/' + name + '.jpg'
        lost_col_ref.document(name).delete()
    img_deleter(path)


def data_cleaner():
    with open('faceless.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            faceless.add(line.replace('\n', ''))
    if not len(faceless):
        for e in faceless:
            path = 'Training_images/' + e + '.jpg'
            delete_imgs(path, False)
    faceless.clear()
    with open('faceless.txt', 'w'):
        pass


while True:
    time.sleep(60)
    print("Waiting for changes")
