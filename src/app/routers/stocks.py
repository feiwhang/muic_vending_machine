from http import HTTPStatus

import ormar
from fastapi import APIRouter, HTTPException

from ..db import VendingMachine, Product

router = APIRouter(
    prefix="/api/stocks",
    tags=["Stocks"]
)


@router.post("/add")
async def add_product_to_stocks(
        vending_machine_id: int, product_id: int, quantity: int
):
    """
    Adds a product to a vending machine's stock by taking a vending machine id, product id, and quantity as input,
    then adds it to the database.
    An error message is returned if the vending machine id or product id does not exist or if an exception occurs during add.
    """
    machine = None
    try:
        # retrieve the vending machine
        machine = await VendingMachine.objects.get(id=vending_machine_id)
    except ormar.NoMatch:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    try:
        # retrieve the product
        product = await Product.objects.get(id=product_id)
        # check if product already exists in the vending machine's stocks
        if await machine.stocks.filter(id=product_id).exists():
            return HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Product already exist in stocks, please edit or delete",
            )
        # add the product to the vending machine's stocks with quantity
        await machine.stocks.add(product, quantity=quantity)

    except ormar.NoMatch:
        return HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Product does not exist, please create"
        )
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Product added to stocks")


@router.get("/stocks")
async def get_stocks(vending_machine_id: int):
    """
    Gets all products in a vending machine by taking a vending machine id as input.
    An error message is returned if the vending machine id does not exist or if an exception occurs during get.
    """
    try:
        machine = await VendingMachine.objects.get(id=vending_machine_id)
        stocks = await machine.stocks.all()
        return [
            {"name": product.name, "quantity": product.stock.quantity}
            for product in stocks
        ]
    except ormar.NoMatch:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/edit")
async def edit_stocks(vending_machine_id: int, product_id: int, new_quantity: int):
    """
    Edits the quantity of a product in a vending machine's stock by taking a vending machine id, product id, and quantity as input.
    An error message is returned if the vending machine id or product id does not exist or if an exception occurs during update.
    """
    try:
        machine = await VendingMachine.objects.get(id=vending_machine_id)
        # check if product exists in the vending machine's stocks
        if not await machine.stocks.filter(id=product_id).exists():
            return HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Product does not exist in stocks, please add",
            )
        await machine.stocks.filter(id=product_id).update(
            stock={"quantity": new_quantity}
        )
    except ormar.NoMatch:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Product quantity updated")


@router.delete("/delete")
async def delete_stocks(vending_machine_id: int, product_id: int):
    """
    Deletes a product from a vending machine's stock by taking a vending machine id and product id as input.
    An error message is returned if the vending machine id or product id does not exist or if an exception occurs during delete.
    """
    try:
        machine = await VendingMachine.objects.get(id=vending_machine_id)
        # check if product exists in the vending machine's stocks
        if not await machine.stocks.filter(id=product_id).exists():
            return HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Product does not exist in stocks",
            )
        await machine.stocks.filter(id=product_id).delete_through_instance(product_id)
    except ormar.NoMatch:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Product deleted from stocks")
