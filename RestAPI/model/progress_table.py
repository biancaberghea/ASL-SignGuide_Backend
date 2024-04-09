from sqlalchemy import MetaData, Table

from RestAPI.app import app
from RestAPI.db.db_init import db

metadata = MetaData()

with app.app_context():
    user_progress = Table('user_progress', metadata, autoload_with=db.engine)

