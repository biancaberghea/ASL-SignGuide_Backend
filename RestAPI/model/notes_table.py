from sqlalchemy import MetaData, Table

from RestAPI.app import app
from RestAPI.db.db_init import db

metadata = MetaData()

with app.app_context():
    notes = Table('notes', metadata, autoload_with=db.engine)
    user_notes = Table('user_notes', metadata, autoload_with=db.engine)
