import ormar
from app.db import database, metadata


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Product(ormar.Model):
    class Meta(BaseMeta):
        tablename = "products"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    price: int = ormar.Integer(minimum=1, nullable=False)


class Stock(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stocks"

    id: int = ormar.Integer(primary_key=True)
    quantity: int = ormar.Integer(minimum=0, nullable=False)


class VendingMachine(ormar.Model):
    class Meta(BaseMeta):
        tablename = "vending_machines"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    location: str = ormar.String(max_length=100, nullable=False)
    stocks = ormar.ManyToMany(Product, through=Stock)
