from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from RestAPI.controller.profile import profile_bp
from RestAPI.service.profile_service import profile_service


@profile_bp.route('/addNotes', methods=['POST'])
def add_note():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')
        profile_service.add_note(title, content, user_id)
        return jsonify({'message': 'Add Note successful'}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Add Note failed'}), 500


@profile_bp.route('/getNotes', methods=['GET'])
def get_notes():
    try:
        user_id = request.args.get('user_id')
        notes_dict = profile_service.get_notes(user_id)
        return jsonify({'notes': notes_dict}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Getting Notes failed'}), 500


@profile_bp.route('/deleteNote', methods=['POST'])
def delete_note():
    try:
        data = request.get_json()
        note = data.get('note')
        user_id = data.get('user_id')

        profile_service.delete_note(user_id, note)
        return jsonify({'message': 'Note Deletion successful'}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Note Deletion failed'}), 500


@profile_bp.route('/editNote', methods=['POST'])
def edit_note():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        note = data.get('note')
        ex_note = data.get('ex_note')
        profile_service.edit_note(user_id, note, ex_note)
        return jsonify({'message': 'Note Edit successful'}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Note Edit failed'}), 500


@profile_bp.route('/updateLearnProgress', methods=['POST'])
def update_learn_progress():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        video_id = data.get('video_id')

        profile_service.update_learn_progress(user_id, video_id)
        return jsonify({'message': 'Learn Progress Update successful'}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Learn Progress Update failed'}), 500


@profile_bp.route('/getLearnPercent', methods=['GET'])
def get_learn_percent():
    try:
        user_id = request.args.get('user_id')
        progress = profile_service.get_learn_percent(user_id)
        return jsonify({'progress': progress}), 200
    except SQLAlchemyError:
        return jsonify({'message': 'Learn Progress Calculation failed'}), 500


@profile_bp.route('/getQuizPercent', methods=['GET'])
def get_quiz_percent():
    try:
        user_id = request.args.get('user_id')
        progress = profile_service.get_quiz_percent(user_id)
        return jsonify({'progress': progress})
    except SQLAlchemyError:
        return jsonify({'message': 'Quiz Progress Calculation failed'}), 500
