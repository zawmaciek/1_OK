from fastapi import FastAPI
from pydantic import BaseModel

from elviron import MatcherFactory, MatcherType

app = FastAPI()
matcher = MatcherFactory.build(type=MatcherType.ELVIRON)


class MovieMatchRequest(BaseModel):
    titles: list[str]


@app.on_event("startup")
def startup_event() -> None:
    matcher.connect_to_db()


@app.post("/calculate")
async def calculate() -> None:
    matcher.calculate()


@app.post("/match")
async def match(request_body: MovieMatchRequest):
    titles = [title for title in request_body.titles]
    result = matcher.match(titles)
    return result


@app.on_event("shutdown")
def shutdown_event() -> None:
    matcher.exit()
