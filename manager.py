import urllib.request
import os

lost_dir = 'Training_images'
found_dir = 'Found_images'


def img_downloader(name, url, found):
    filename = name + '.jpg'
    if found:
        filepath = found_dir + '/' + filename
    else:
        filepath = lost_dir + '/' + filename

    if not os.path.exists(lost_dir):
        os.mkdir(lost_dir)

    if not os.path.exists(found_dir):
        os.mkdir(found_dir)

    if not os.path.isfile(filepath):
        urllib.request.urlretrieve(url, filepath)


def img_deleter(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        print("NO SUCH FILE EXISTS")

