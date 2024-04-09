from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from RestAPI.controller.categories import cat_bp
from RestAPI.service.categories_service import cat_service


@cat_bp.route('/getCategories', methods=['GET'])
def get_categories():
    try:
        organized_cats = cat_service.get_cats()
        return jsonify({'cats': organized_cats}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Getting cats failed'}), 500


@cat_bp.route('/getDataForCategory', methods=['GET'])
def get_cat_content():
    try:
        selected_category = request.args.get('category')
        cat_content = cat_service.get_cat_content(selected_category)
        return jsonify({'cat_content': cat_content}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Getting cat content failed'}), 500


@cat_bp.route('/check-url', methods=['GET'])
def check_url():
    url = request.args.get('url')
    return cat_service.check_url(url)


@cat_bp.route('/getVideoId', methods=['GET'])
def get_video_id():
    try:
        word = request.args.get('word')
        video_id = cat_service.get_video_id(word)
        return jsonify({'video_id': video_id}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Getting video id failed'}), 500


@cat_bp.route('/load-items', methods=['GET'])
def load_items():
    try:
        page_nr = request.args.get('pageNr')
        page_size = request.args.get('pageSize')
        item_list = cat_service.load_items(page_size, page_nr)
        return jsonify({'items': [item.to_json() for item in item_list]})
    except SQLAlchemyError:
        return jsonify({'message': 'Loading items failed'}), 500


@cat_bp.route('/getItemsLen', methods=['GET'])
def get_items_len():
    try:
        len = cat_service.get_items_len()
        return jsonify({'len': len}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Getting items len failed'}), 500


@cat_bp.route('/editItem', methods=['POST'])
def edit_item():
    try:
        data = request.get_json()
        ex_item = data.get('item')
        new_item = data.get('new_item')

        cat_service.edit_item(ex_item, new_item)
        return jsonify({'message': 'Item Edit successful'}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Item Edit failed'}), 500


@cat_bp.route('/deleteItem', methods=['POST'])
def delete_item():
    try:
        data = request.get_json()
        item = data.get('item')
        cat_service.delete_item(item)
        return jsonify({'message': 'Item Deletion successful'}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Item Deletion failed'}), 500


@cat_bp.route('/addItem', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        item = data.get('item')
        cat_service.add_item(item)
        return jsonify({'message': 'Add Item successful'}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Add Item failed'}), 500


@cat_bp.route('/searchWord', methods=['GET'])
def search_word():
    try:
        word = request.args.get('word')
        url = cat_service.search_word(word)
        return jsonify({'url': url}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Searching word failed'}), 500


@cat_bp.route('/searchItem', methods=['GET'])
def search_item():
    try:
        search_text = request.args.get('searchText')
        item_list = cat_service.search_item(search_text)
        return jsonify({'items': [item.to_json() for item in item_list]})
    except SQLAlchemyError:
        return jsonify({'message': 'Searching item failed'}), 500
