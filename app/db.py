from typing import Optional, Dict
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
    class Meta(BaseMeta):
        tablename = "products"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    price: int = ormar.Integer(minimum=1, nullable=False)


class VendingMachine(ormar.Model):
    class Meta(BaseMeta):
        tablename = "vending_machines"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    location: str = ormar.String(max_length=100, nullable=False)
    stocks = ormar.ManyToMany(
        Product,
        through_relation_name="vending_machine_id",
        through_reverse_relation_name="product_id",
    )


class VendingMachineXProduct(ormar.Model):
    class Meta(BaseMeta):
        tablename = "vending_machines_x_products"

    quantity: int = ormar.Integer(minimum=1, nullable=False)
    vending_machine_id = ormar.ForeignKey(VendingMachine)
    product_id = ormar.ForeignKey(Product)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
