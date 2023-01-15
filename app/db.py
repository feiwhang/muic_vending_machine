from typing import Optional, List
from .config import settings

import databases
import ormar
import sqlalchemy

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Product(ormar.Model):
    class Meta():
        tablename = 'products'
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)


class VendingMachine(ormar.Model):
    class Meta():
        tablename = 'vending_machines'
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    location: str = ormar.String(max_length=100, nullable=False)
    products: Optional[List[Product]] = ormar.ManyToMany(Product)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)