"""This module contains the stocks router."""
from http import HTTPStatus

import ormar
from fastapi import APIRouter, HTTPException

from ..constants import VENDING_MACHINE_NOT_FOUND_MSG
from ..db import Product, VendingMachine

router = APIRouter(prefix="/api/stocks", tags=["Stocks"])


@router.post("/add")
async def add_product_to_stocks(vending_machine_id: int, product_id: int, quantity: int) -> dict:
    """Add a product to a vending machine's stock.

    Args:
        vending_machine_id (int): The id of the vending machine.
        product_id (int): The id of the product.
        quantity (int): The quantity of the product to add.

    Returns:
        dict: a dict showing if operation is successful.
    """
    machine = None
    try:
        # retrieve the vending machine
        machine = await VendingMachine.objects.get(id=vending_machine_id)
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    try:
        # retrieve the product
        product = await Product.objects.get(id=product_id)
        # check if product already exists in the vending machine's stocks
        if await machine.stocks.filter(id=product_id).exists():
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Product already exist in stocks, please edit or delete",
            )
        # add the product to the vending machine's stocks with quantity
        await machine.stocks.add(product, quantity=quantity)

        return {"ok": True}
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Product does not exist, please create",
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/stocks")
async def get_stocks(vending_machine_id: int) -> list:
    """Get all products in a vending machine.

    Args:
        vending_machine_id (int): The id of the vending machine.

    Returns:
        list: A list of products in the vending machine
    """
    try:
        machine = await VendingMachine.objects.get(id=vending_machine_id)
        stocks = await machine.stocks.all()

        return [{"name": product.name, "quantity": product.stock.quantity} for product in stocks]
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/edit")
async def edit_stocks(vending_machine_id: int, product_id: int, new_quantity: int) -> dict:
    """Edit the quantity of a product in a vending machine's stock.

    Args:
        vending_machine_id (int): The id of the vending machine.
        product_id (int): The id of the product.
        new_quantity (int): The new quantity of the product.

    Returns:
        dict: A dict showing if operation is successful.
    """
    machine = None
    try:
        machine = await VendingMachine.objects.get(id=vending_machine_id)
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    try:
        # check if product exists in the vending machine's stocks
        if not await machine.stocks.filter(id=product_id).exists():
            raise ormar.NoMatch
        await machine.stocks.filter(id=product_id).update(stock={"quantity": new_quantity})

        return {"ok": True}
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Product does not exist, please create",
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete")
async def delete_stocks(vending_machine_id: int, product_id: int) -> dict:
    """Delete a product from a vending machine's stock.

    Args:
        vending_machine_id (int): The id of the vending machine.
        product_id (int): The id of the product.

    Returns:
        dict: a dict showing if the operation was successful.
    """
    try:
        machine = await VendingMachine.objects.get(id=vending_machine_id)
        # check if product exists in the vending machine's stocks
        if not await machine.stocks.filter(id=product_id).exists():
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Product does not exist in stocks",
            )
        await machine.stocks.filter(id=product_id).delete_through_instance(product_id)

        return {"ok": True}
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
