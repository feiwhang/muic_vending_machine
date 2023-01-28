"""Database connection and models."""
import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    """Base metadata for all models."""

    metadata = metadata
    database = database


class Product(ormar.Model):
    """Product model."""

    class Meta(BaseMeta):
        """Meta class for Product model."""

        tablename = "products"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    price: int = ormar.Integer(minimum=1, nullable=False)


class Stock(ormar.Model):
    """Stock model."""

    class Meta(BaseMeta):
        """Meta class for Stock model."""

        tablename = "stocks"

    id: int = ormar.Integer(primary_key=True)
    quantity: int = ormar.Integer(minimum=0, nullable=False)


class VendingMachine(ormar.Model):
    """Vending machine model."""

    class Meta(BaseMeta):
        """Meta class for VendingMachine model."""

        tablename = "vending_machines"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    location: str = ormar.String(max_length=100, nullable=False)
    stocks = ormar.ManyToMany(Product, through=Stock)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
