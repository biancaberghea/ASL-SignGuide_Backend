from sqlalchemy import select, update, delete, insert, literal
from sqlalchemy.exc import SQLAlchemyError

from RestAPI.db.db_init import db
from RestAPI.model.item_table import items
from RestAPI.model.progress_table import user_progress
from RestAPI.model.user import User


def get_cats():
    query = select(items.c.cat).distinct()
    result = db.session.execute(query)
    return result.fetchall()


def get_cat_content(selected_category):
    query = select(items).where(items.c.cat == selected_category)
    result = db.session.execute(query)
    return result.fetchall()


def get_video_id(word):
    query = select(items.c.id).where(items.c.word == word)
    result = db.session.execute(query)
    row = result.fetchall()[0]
    video_id = row[0]
    return video_id


def load_items(page_size, page_nr):
    try:
        query = select(items).limit(page_size).offset((int(page_nr) - 1) * int(page_size))
        result = db.session.execute(query)
        return result.fetchall()
    except SQLAlchemyError:
        return []


def get_items_len():
    return db.session.query(db.func.count()). \
        select_from(items).scalar()


def get_item_id(word, url, cat):
    query_id = select(items.c.id).where(
        db.and_(items.c.url == url, items.c.cat == cat, items.c.word == word))
    result_id = db.session.execute(query_id)
    row = result_id.fetchall()[0]
    id = row[0]
    return id


def edit_item(id, word, url, cat):
    query_update = update(items).where(items.c.id == id).values(word=word, url=url, cat=cat)
    db.session.execute(query_update)
    db.session.commit()


def delete_item(id):
    query_delete_user_progress = delete(user_progress).where(user_progress.c.word_id == id)
    db.session.execute(query_delete_user_progress)

    query_delete_word = delete(items).where(items.c.id == id)
    db.session.execute(query_delete_word)
    db.session.commit()


def add_item(word, url, cat):
    query_insert = insert(items).values(word=word, url=url, cat=cat)
    result_proxy = db.session.execute(query_insert)
    db.session.commit()

    new_item_id = result_proxy.lastrowid

    select_query = select(
        User.__table__.c.id.label('user_id'),
        literal(new_item_id).label('word_id'),
        literal(0).label('learned'), literal(0).label('correct_quiz')
    )

    query_insert_user_progress = insert(user_progress).from_select(
        ['user_id', 'word_id', 'learned', 'correct_quiz'],
        select_query)
    db.session.execute(query_insert_user_progress)
    db.session.commit()


def search_word(word):
    query = select(items.c.url).where(items.c.word == word)
    result = db.session.execute(query)
    return result.fetchall()


def search_item(search_text):
    query = select(items). \
        where(db.or_(items.c.word == search_text, items.c.url == search_text, items.c.cat == search_text))

    result = db.session.execute(query)
    return result.fetchall()
