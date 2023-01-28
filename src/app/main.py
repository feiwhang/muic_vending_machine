from fastapi import FastAPI
from .db import database, VendingMachine, Product, Stock

from .routers import vending_machines, products, stocks

app = FastAPI(title="MUIC Vending Machine")

app.include_router(vending_machines.router)
app.include_router(products.router)
app.include_router(stocks.router)


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
