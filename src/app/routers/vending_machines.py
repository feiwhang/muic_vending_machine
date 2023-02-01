"""This module contains the routes for vending machines."""
from http import HTTPStatus

import asyncpg
import ormar
from fastapi import APIRouter, HTTPException

from ..constants import VENDING_MACHINE_NOT_FOUND_MSG
from ..db import VendingMachine

router = APIRouter(prefix="/api/vending_machines", tags=["Vending Machines"])


@router.post("/create")
async def create_vending_machine(name: str, location: str) -> VendingMachine:
    """Create a new vending machine.

    Args:
        name (str): The name of the vending machine.
        location (str): The location of the vending machine.

    Returns:
        VendingMachine: A newly created vending machine.
    """
    try:
        new_machine = VendingMachine(name=name, location=location)
        await new_machine.save()

        return new_machine
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Vending machine name already exists",
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/edit")
async def edit_vending_machine(machine_id: int, new_name: str | None = None, new_location: str | None = None) -> dict:
    """Edit the name of a vending machine.

    Args:
        machine_id (int): The id of the vending machine to edit.
        new_name (str, optional): The new name of the vending machine. Defaults to None.
        new_location (str, optional): The new location of the vending machine. Defaults to None.

    Returns:
        dict: A dictionary containing the status of the operation.
    """
    try:
        machine = await VendingMachine.objects.get(id=machine_id)
        if new_name or new_location:
            machine.name = new_name or machine.name
            machine.location = new_location or machine.location
            await machine.update()

            return {"ok": True}
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="No new name or location provided",
        )
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete")
async def delete_vending_machine(machine_id: int) -> dict:
    """Delete a vending machine.

    Args:
        machine_id (int): The id of the vending machine to delete.

    Returns:
        dict: A dictionary containing the status of the operation.
    """
    try:
        machine: VendingMachine = await VendingMachine.objects.get(machine_id=machine_id)
        await machine.delete()

        return {"ok": True}
    except ormar.NoMatch:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=VENDING_MACHINE_NOT_FOUND_MSG,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
