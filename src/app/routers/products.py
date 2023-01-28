from http import HTTPStatus

import asyncpg
from fastapi import APIRouter, HTTPException

from ..db import Product

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post("/create")
async def create_product(name: str, price: int):
    """
    Creates a new product by taking a name and price as input, then saves it to the database.
    An error message is returned if the product name already exists or if an exception occurs during save.
    """
    try:
        new_product = Product(name=name, price=price)
        await new_product.save()
    except asyncpg.exceptions.UniqueViolationError:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Product name already exists")
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Product created")


@router.get("/all")
async def get_products():
    """
    Gets all products in the database.
    """
    products = await Product.objects.all()
    return [{"id": product.id, "name": product.name, "price": product.price} for product in products]
