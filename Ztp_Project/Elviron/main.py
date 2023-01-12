from fastapi import FastAPI
from pydantic import BaseModel

from elviron import Elviron

app = FastAPI()
elviron = Elviron()


class MovieMatchRequest(BaseModel):
    titles: list[str]


@app.on_event("startup")
def startup_event() -> None:
    elviron.connect_to_db()


@app.post("/calculate")
async def calculate() -> None:
    elviron.calculate()


@app.post("/match")
async def match(request_body: MovieMatchRequest):
    titles = [title for title in request_body.titles]
    result = elviron.match(titles)
    return result


@app.on_event("shutdown")
def shutdown_event() -> None:
    elviron.exit()
