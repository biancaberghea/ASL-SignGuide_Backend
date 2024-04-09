from RestAPI.repository.categories_repo import cat_repo
from RestAPI.repository.profile_repo import profile_repo


def add_note(title, content, user_id):
    profile_repo.add_note(title, content, user_id)


def get_notes(user_id):
    return profile_repo.get_notes(user_id)


def delete_note(user_id, note):
    note_id = profile_repo.find_note_id_for_user(note, user_id)
    profile_repo.delete_note(note_id)


def edit_note(user_id, note, ex_note):
    key = list(note.keys())[0]
    if isinstance(note[key], list):
        value = note[key][0]
    else:
        value = note[key]

    ex_note_id = profile_repo.find_note_id_for_user(ex_note, user_id)
    profile_repo.edit_note(ex_note_id, key, value)


def update_learn_progress(user_id, video_id):
    profile_repo.update_learn_progress(user_id, video_id)


def get_learn_percent(user_id):
    learned_words = profile_repo.get_learn_percent(user_id)
    len_items = cat_repo.get_items_len()
    progress = (learned_words * 100) / len_items
    return progress


def get_quiz_percent(user_id):
    taken_quiz = profile_repo.get_quiz_percent(user_id)
    len_items = cat_repo.get_items_len()
    progress = (taken_quiz * 100) / len_items
    return progress
