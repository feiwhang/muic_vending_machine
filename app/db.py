from .config import settings

import databases
import sqlalchemy

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
