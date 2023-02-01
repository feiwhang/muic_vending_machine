"""This module contains the routes for the products."""
from http import HTTPStatus

import asyncpg
from fastapi import APIRouter, HTTPException

from ..db import Product

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("/create")
async def create_product(name: str, price: int) -> Product:
    """Create a new product.

    Args:
        name (str): The name of the product.
        price (int): The price of the product.

    Returns:
        Product: The newly created product.
    """
    try:
        new_product = Product(name=name, price=price)
        await new_product.save()

        return new_product
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Product name already exists",
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/all")
async def get_products() -> list:
    """Get all products in the database."""
    products = await Product.objects.all()
    return [{"id": product.id, "name": product.name, "price": product.price} for product in products]
