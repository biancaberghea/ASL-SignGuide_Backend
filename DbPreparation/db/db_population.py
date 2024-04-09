import json

from sqlalchemy import insert

from RestAPI.db.db_init import db
from RestAPI.model.item_table import items


def populate_db():
    with open('../../words.json', 'r') as file:
        data = json.load(file)
        for item in data:
            query = insert(items).values(word=item["word"], url=item["url"], cat=item["cat"])
            db.session.execute(query)
        db.session.commit()
