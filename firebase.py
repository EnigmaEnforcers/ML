import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from manager import img_downloader
import asyncio


cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://accenture-578fc-default-rtdb.firebaseio.com"
})
dbref = db.reference("/lost") 
lost = dbref.get()


async def get_imgs():
    print("Downloading recent uploads")
    for key, value in lost.items():
        img_downloader(key, value['image'], False)
    print("Download Complete")


async def delete_img(filename):
    s = filename.split('/')
    key = s[-1].split('.')
    print(key[0])
    dbref.child(key[0]).remove()

