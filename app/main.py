from fastapi import FastAPI, HTTPException
from app.db import database, VendingMachine, Product, Stock

import ormar
import asyncpg

app = FastAPI(title="MUIC Vending Machine")


@app.get("/")
async def read_root():
    return {
        "Vending Machine": await VendingMachine.objects.all(),
        "Product": await Product.objects.all(),
        "Stocks": await Stock.objects.all(),
    }


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.post("/vending_machine/create")
async def create_vending_machine(name: str, location: str):
    """
    Creates a new vending machine by taking a name and location as input, then saves it to the database.
    An error message is returned if the vending machine name already exists or if an exception occurs during save.
    """
    try:
        new_machine = VendingMachine(name=name, location=location)
        await new_machine.save()
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=500, detail="Vending machine name already exists"
        )
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return HTTPException(status_code=200, detail="Vending machine created")


@app.put("/vending_machine/edit")
async def edit_vending_machine(
    id: int, new_name: str | None = None, new_location: str | None = None
):
    """
    Edits the name of a vending machine by taking an id and name as input, then saves it to the database.
    An error message is returned if the vending machine id does not exist or if an exception occurs during update.
    Only update when there's any new data.
    """
    try:
        machine = await VendingMachine.objects.get(id=id)
        if new_name or new_location:
            machine.name = new_name or machine.name
            machine.location = new_location or machine.location
            await machine.update()
    except ormar.NoMatch:
        return HTTPException(status_code=500, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return HTTPException(status_code=200, detail="Vending machine updated")


@app.delete("/vending_machine/delete")
async def delete_vending_machine(id: int):
    """
    Deletes a vending machine by taking an id as input, then deteles it from the database.
    An error message is returned if the vending machine id does not exist or if an exception occurs during delete.
    """
    try:
        machine: VendingMachine = await VendingMachine.objects.get(id=id)
        await machine.delete()
    except ormar.NoMatch:
        return {"error_message": "Vending machine does not exist"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return HTTPException(status_code=200, detail="Vending machine deleted")


@app.post("/vending_machine/stocks/add")
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
        return HTTPException(status_code=500, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

    try:
        # retrieve the product
        product = await Product.objects.get(id=product_id)
        # check if product already exists in the vending machine's stocks
        if await machine.stocks.filter(id=product_id).exists():
            return HTTPException(
                status_code=500,
                detail="Product already exist in stocks, please edit or delete",
            )
        # add the product to the vending machine's stocks with quantity
        await machine.stocks.add(product, quantity=quantity)

    except ormar.NoMatch:
        return HTTPException(
            status_code=500, detail="Product does not exist, please create"
        )
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return HTTPException(status_code=200, detail="Product added to stocks")


@app.get("/vending_machine/stocks")
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
        return HTTPException(status_code=500, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.put("/vending_machine/stocks/edit")
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
                status_code=500,
                detail="Product does not exist in stocks, please add",
            )
        await machine.stocks.filter(id=product_id).update(
            stock={"quantity": new_quantity}
        )
    except ormar.NoMatch:
        return HTTPException(status_code=500, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return HTTPException(status_code=200, detail="Product quantity updated")


@app.post("/product/create")
async def create_product(name: str, price: int):
    """
    Creates a new product by taking a name and price as input, then saves it to the database.
    An error message is returned if the product name already exists or if an exception occurs during save.
    """
    try:
        new_product = Product(name=name, price=price)
        await new_product.save()
    except asyncpg.exceptions.UniqueViolationError:
        return HTTPException(status_code=500, detail="Product name already exists")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return HTTPException(status_code=200, detail="Product created")
