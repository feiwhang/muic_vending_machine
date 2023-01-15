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
