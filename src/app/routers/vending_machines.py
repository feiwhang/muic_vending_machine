from http import HTTPStatus

import asyncpg
import ormar
from fastapi import APIRouter, HTTPException

from ..db import VendingMachine

router = APIRouter(
    prefix="/api/vending_machines",
    tags=["Vending Machines"]
)


@router.post("/create")
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
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Vending machine name already exists"
        )
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Vending machine created")


@router.put("/edit")
async def edit_vending_machine(
        machine_id: int, new_name: str | None = None, new_location: str | None = None
):
    """
    Edits the name of a vending machine by taking an id and name as input, then saves it to the database.
    An error message is returned if the vending machine id does not exist or if an exception occurs during update.
    Only update when there's any new data.
    """
    try:
        machine = await VendingMachine.objects.get(id=machine_id)
        if new_name or new_location:
            machine.name = new_name or machine.name
            machine.location = new_location or machine.location
            await machine.update()
    except ormar.NoMatch:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Vending machine does not exist")
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Vending machine updated")


@router.delete("/delete")
async def delete_vending_machine(machine_id: int):
    """
    Deletes a vending machine by taking an id as input, then deletes it from the database.
    An error message is returned if the vending machine id does not exist or if an exception occurs during delete.
    """
    try:
        machine: VendingMachine = await VendingMachine.objects.get(machine_id=machine_id)
        await machine.delete()
    except ormar.NoMatch:
        return {"error_message": "Vending machine does not exist"}
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Vending machine deleted")
