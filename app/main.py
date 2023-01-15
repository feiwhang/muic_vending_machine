from fastapi import FastAPI
from app.db import database, VendingMachine

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
    An error message is returned if the vending machine name already exists or if an exception occurs during the save operation.
    """
    new_machine = VendingMachine(name=name, location=location)
    try:
        await new_machine.save()
    except Exception as e:
        return {"error_message": e.message}
    return new_machine
