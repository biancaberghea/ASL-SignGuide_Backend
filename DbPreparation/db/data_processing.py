import json

import requests

from DbPreparation.model.item import Item


def check_url(url):
    try:
        response = requests.get(url, allow_redirects=False)
        return response.status_code == 200
    except:
        return False


def check_embed(url):
    try:
        response = requests.head(url)
        x_frame_options = response.headers.get('X-Frame-Options')
        if x_frame_options == 'sameorigin' or x_frame_options == 'DENY':
            return False
        else:
            return True
    except Exception:
        return False


def check_content_type(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('Content-Type')
        if 'video' not in content_type:
            return False
        else:
            return True
    except Exception:
        return False


def populate_db():
    yts = []
    items = []
    with open('../../WLASL_v0.3.json', 'r') as file:
        data = json.load(file)
        for dataline in data:
            found = False
            for instance in dataline["instances"]:
                if 'youtube' in instance["url"]:
                    yts.append(instance["url"])
                elif check_url(instance["url"]) and check_embed(instance["url"]) and check_content_type(
                        instance["url"]):
                    i = Item(dataline["gloss"], instance["url"])
                    items.append(i)
                    found = True
                    break
            if not found:
                for yt in yts:
                    if check_url(yt) and check_embed(yt) and check_content_type(yt):
                        i = Item(dataline["gloss"], yt)
                        items.append(i)
                        break

    with open('../../words.json', 'w') as output_file:
        json.dump(items, output_file)
