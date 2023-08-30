import requests
import os


lost_dir = 'notebook/data/lost_images'


def img_downloader(name, url):
    filename = name + '.jpg'
    filepath = lost_dir + '/' + filename
    if not os.path.exists('notebook/data'):
        os.mkdir('notebook/data')

    if not os.path.exists(lost_dir):
        os.mkdir(lost_dir)

    if not os.path.isfile(filepath):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
