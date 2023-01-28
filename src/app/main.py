"""Main module for the application."""
from fastapi import FastAPI

from .db import Product, Stock, VendingMachine, database
from .routers import products, stocks, vending_machines

app = FastAPI(title="MUIC Vending Machine")

app.include_router(vending_machines.router)
app.include_router(products.router)
app.include_router(stocks.router)


@app.get("/")
async def read_root() -> dict:
    """Return all data in the database."""
    return {
        "Vending Machine": await VendingMachine.objects.all(),
        "Product": await Product.objects.all(),
        "Stocks": await Stock.objects.all(),
    }


@app.on_event("startup")
async def startup() -> None:
    """Connect to the database on startup."""
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Disconnect from the database on shutdown."""
    if database.is_connected:
        await database.disconnect()
