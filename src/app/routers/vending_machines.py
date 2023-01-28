"""This module contains the routes for vending machines."""
from http import HTTPStatus

import asyncpg
import ormar
from fastapi import APIRouter, HTTPException

from ..constants import VENDING_MACHINE_NOT_FOUND_MSG
from ..db import VendingMachine

router = APIRouter(prefix="/api/vending_machines", tags=["Vending Machines"])


@router.post("/create")
async def create_vending_machine(name: str, location: str) -> HTTPException:
    """Create a new vending machine.

    Args:
        name (str): The name of the vending machine.
        location (str): The location of the vending machine.

    Returns: HTTPException: An error message is returned if the vending machine name already exists or if an
                            exception occurs during save.
    """
    try:
        new_machine = VendingMachine(name=name, location=location)
        await new_machine.save()
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Vending machine name already exists",
        )
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Vending machine created")


@router.put("/edit")
async def edit_vending_machine(
    machine_id: int, new_name: str | None = None, new_location: str | None = None
) -> HTTPException:
    """Edit the name of a vending machine.

    Args:
        machine_id (int): The id of the vending machine to edit.
        new_name (str, optional): The new name of the vending machine. Defaults to None.
        new_location (str, optional): The new location of the vending machine. Defaults to None.

    Returns:
        HTTPException: An HTTPException with the status code and detail message.
    """
    try:
        machine = await VendingMachine.objects.get(id=machine_id)
        if new_name or new_location:
            machine.name = new_name or machine.name
            machine.location = new_location or machine.location
            await machine.update()
    except ormar.NoMatch:
        return HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Vending machine updated")


@router.delete("/delete")
async def delete_vending_machine(machine_id: int) -> HTTPException:
    """Delete a vending machine.

    Args:
        machine_id (int): The id of the vending machine to delete.

    Returns:
        HTTPException: An HTTPException with the status code and detail message.
    """
    try:
        machine: VendingMachine = await VendingMachine.objects.get(machine_id=machine_id)
        await machine.delete()
    except ormar.NoMatch:
        return HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return HTTPException(status_code=HTTPStatus.OK, detail="Vending machine deleted")
