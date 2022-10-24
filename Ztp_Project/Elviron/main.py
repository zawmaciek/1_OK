from fastapi import FastAPI

from elviron import Elviron

app = FastAPI()
elviron = Elviron()


@app.on_event("startup")
def startup_event() -> None:
    elviron.connect_to_db()


@app.post("/calculate")
async def calculate() -> None:
    elviron.calculate()


@app.get("/match")
async def match():
    result = elviron.match()
    return result


@app.on_event("shutdown")
def shutdown_event() -> None:
    elviron.exit()
