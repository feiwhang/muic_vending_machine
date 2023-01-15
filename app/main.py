from fastapi import FastAPI
from app.db import database, VendingMachine

import ormar
import asyncpg

app = FastAPI(title="MUIC Vending Machine")


@app.get("/")
async def read_root():
    return await VendingMachine.objects.all()


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
    new_machine = VendingMachine(name=name, location=location)
    try:
        await new_machine.save()
    except asyncpg.exceptions.UniqueViolationError:
        return {"error_message": "Vending machine name already exists"}
    except Exception as e:
        return {"error_message": e.message}
    return new_machine


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
        return {"error_message": "Vending machine does not exist"}
    except Exception as e:
        return {"error_message": e.message}
    return machine


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
        return {"error_message": e.message}
    return machine
