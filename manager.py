import urllib.request
import os

lost_dir = 'data/lost_images'


def img_downloader(name, url):
    filename = name + '.jpg'
    filepath = lost_dir + '/' + filename
    if not os.path.exists('data'):
        os.mkdir('data')

    if not os.path.exists(lost_dir):
        os.mkdir(lost_dir)

    if not os.path.isfile(filepath):
        urllib.request.urlretrieve(url, filepath)


def img_deleter(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        print("NO SUCH FILE EXISTS")

