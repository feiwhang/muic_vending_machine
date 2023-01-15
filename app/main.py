from fastapi import FastAPI

app = FastAPI(title="MUIC Vending Machine")


@app.get("/")
def read_root():
    return {"main": "app"}
