import requests
from flask import jsonify

from RestAPI.model.Item import Item
from RestAPI.repository.categories_repo import cat_repo


def organize_by_cat(cats):
    organized_cats = {
        'Adjectives': [],
        'Adverbs': [],
        'Verbs': [],
        'Nouns': [],
        'Phrases': []
    }

    for cat in cats:
        if cat == 'NULL':
            break
        elif 'adverb' in cat:
            organized_cats['Adverbs'].append(cat.title())
        elif 'verb' in cat:
            organized_cats['Verbs'].append(cat.title())
        elif 'adjective' in cat:
            organized_cats['Adjectives'].append(cat.title())
        elif 'phrase' in cat:
            organized_cats['Phrases'].append(cat.title())
        else:
            organized_cats['Nouns'].append(cat.title())
    return organized_cats


def get_cats():
    rows = cat_repo.get_cats()
    rows = [row for row in rows if row[0] is not None]
    cats = [row[0].strip() for row in rows]
    organized_cats = organize_by_cat(cats)
    return organized_cats


def get_cat_content(selected_catgeory):
    rows = cat_repo.get_cat_content(selected_catgeory)
    cat_content = [{"name": row[1], "url": row[2]} for row in rows]
    return cat_content


def check_url(url):
    try:
        response = requests.head(url)
        x_frame_options = response.headers.get('X-Frame-Options')
        content_type = response.headers.get('Content-Type')
        if x_frame_options == 'sameorigin' or x_frame_options == 'DENY' or 'video' not in content_type:
            return jsonify({'allowEmbed': False})
        else:
            return jsonify({'allowEmbed': True})
    except Exception as e:
        print('Error:', e)
        return jsonify({'error': 'Error checking URL'}), 500


def get_video_id(word):
    return cat_repo.get_video_id(word)


def load_items(page_size, page_nr):
    rows = cat_repo.load_items(page_size, page_nr)
    item_list = [Item(row[1], row[2], (row[3].title() if row[3] is not None else row[3])) for row in rows]
    return item_list


def get_items_len():
    return cat_repo.get_items_len()


def edit_item(ex_item, new_item):
    new_key = list(new_item.keys())[0]
    id = cat_repo.get_item_id(ex_item['word'], ex_item['url'], ex_item['cat'])
    cat_repo.edit_item(id, new_key, new_item[new_key][0], new_item[new_key][1])


def delete_item(item):
    id = cat_repo.get_item_id(item['word'], item['url'], item['cat'])
    cat_repo.delete_item(id)


def add_item(item):
    word = list(item.keys())[0]
    url = item[word][0]
    cat = item[word][1]
    cat_repo.add_item(word, url, cat)


def search_word(word):
    rows = cat_repo.search_word(word)
    if len(rows) > 0:
        url = rows[0][0]
        return url
    else:
        return 'Could not find word'


def search_item(search_text):
    rows = cat_repo.search_item(search_text)
    item_list = [Item(row[1], row[2], (row[3].title() if row[3] is not None else row[3])) for row in rows]
    return item_list
