from fastapi import FastAPI
from pydantic import BaseModel

from elviron import Elviron
from movie import MovieID

app = FastAPI()
elviron = Elviron()
class MovieMatchRequest(BaseModel):
    ids: list[int]

@app.on_event("startup")
def startup_event() -> None:
    elviron.connect_to_db()


@app.post("/calculate")
async def calculate() -> None:
    elviron.calculate()


@app.post("/match")
async def match(request_body:MovieMatchRequest):
    ids = [MovieID(id) for id in request_body.ids]
    result = elviron.match(ids)
    return result


@app.on_event("shutdown")
def shutdown_event() -> None:
    elviron.exit()
