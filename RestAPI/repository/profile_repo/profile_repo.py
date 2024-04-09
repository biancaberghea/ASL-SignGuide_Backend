from sqlalchemy import insert, select, join, delete, update

from RestAPI.db.db_init import db
from RestAPI.model.notes_table import notes, user_notes
from RestAPI.model.progress_table import user_progress


def add_note(title, content, user_id):
    query_note = insert(notes).values(title=title, content=content)
    result = db.session.execute(query_note)
    note_id = result.inserted_primary_key[0]

    query_user_note = insert(user_notes).values(user_id=user_id, note_id=note_id)
    db.session.execute(query_user_note)
    db.session.commit()


def get_notes(user_id):
    notes_dict = {}
    query_user_notes = select(user_notes.c.note_id).where(user_notes.c.user_id == user_id)
    result = db.session.execute(query_user_notes)
    rows = result.fetchall()
    for row in rows:
        query_notes = select(notes).where(notes.c.id == row[0])
        note_result = db.session.execute(query_notes)
        note_rows = note_result.fetchall()[0]
        if note_rows[1] not in notes_dict:
            notes_dict[note_rows[1]] = [note_rows[2]]
        else:
            notes_dict[note_rows[1]].append(note_rows[2])

    return notes_dict


def find_note_id_for_user(note, user_id):
    query_notes = (
        select(notes.c.id)
        .select_from(
            join(notes, user_notes, notes.c.id == user_notes.c.note_id)
        )
        .where(
            (notes.c.title == note) &
            (user_notes.c.user_id == user_id)
        )
    )
    result = db.session.execute(query_notes)
    row = result.fetchall()[0]

    return row[0]


def delete_note(note_id):
    query_delete_user_notes = delete(user_notes).where(user_notes.c.note_id == note_id)
    db.session.execute(query_delete_user_notes)
    query_delete_note = delete(notes).where(notes.c.id == note_id)
    db.session.execute(query_delete_note)
    db.session.commit()


def edit_note(ex_note_id, key, value):
    query_update = update(notes).where(notes.c.id == ex_note_id).values(title=key, content=value)
    db.session.execute(query_update)
    db.session.commit()


def update_learn_progress(user_id, video_id):
    query = update(user_progress). \
        where(db.and_(user_progress.c.user_id == user_id, user_progress.c.word_id == video_id)).values(learned=True)
    db.session.execute(query)
    db.session.commit()


def get_learn_percent(user_id):
    return db.session.query(db.func.count()). \
        select_from(user_progress). \
        filter(user_progress.c.user_id == user_id). \
        filter(user_progress.c.learned == True).scalar()


def get_quiz_percent(user_id):
    return db.session.query(db.func.count()). \
        select_from(user_progress). \
        filter(user_progress.c.user_id == user_id). \
        filter(user_progress.c.correct_quiz == True).scalar()
