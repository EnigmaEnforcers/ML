import urllib.request
import os

lost_dir = 'data/lost_images'


def img_downloader(name, url):
    filename = name + '.jpg'
    filepath = lost_dir + '/' + filename
    if not os.path.isfile(filepath):
        urllib.request.urlretrieve(url, filepath)
