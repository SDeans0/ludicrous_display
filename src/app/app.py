from http import HTTPStatus
import logging
import os
import random

import datetime as dt

from beanie.odm.operators.find.logical import Or
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import start_beanie_session
from db.gpt import Bluff
from football_api.actions import persist_transfers
from livescore_api.actions import persist_matches
from gpt.actions.refresh_bluffs import refresh_bluffs
from utils.dateutils import get_start_of_day

WORKING_DIR = os.environ.get('SRC_DIR','/workspace/src')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_beanie_session()

security = HTTPBearer()

def check_access_token(token: HTTPBasicCredentials = Depends(security)):
    authorised =  token.credentials == os.environ.get("API_KEY")

    if not authorised:
        logger.error(f"Could not validate credentials: {token.credentials}")
        raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED.value,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

templates = Jinja2Templates(directory=f"{WORKING_DIR}/app/templates")


@app.get("/", response_class=HTMLResponse)
async def get_bluff(request: Request):
    sod = get_start_of_day()
    n_latest: Bluff = await Bluff.find(Bluff.date >= sod).count()
    while n_latest == 0:
        sod = sod - dt.timedelta(days=1)
        n_latest: Bluff = await Bluff.find(Bluff.date >= sod).count()
    logger.info(f"n_latest: {n_latest}")
    skip = random.randint(0, n_latest-1)
    latest: Bluff = await Bluff.find(Bluff.date >= sod).skip(skip).first_or_none()
    lines = latest.message.split("\n")
    return templates.TemplateResponse("bluff.html", {"request":request, "bluff_lines": lines})


@app.get("/country/{country}", response_class=HTMLResponse)
async def get_bluff(request: Request, country: str):
    sod = get_start_of_day()
    n_latest: Bluff = await Bluff.find(Bluff.date >= sod, Bluff.country == country).count()
    while n_latest == 0:
        sod = sod - dt.timedelta(days=1)
        n_latest: Bluff = await Bluff.find(Bluff.date >= sod, Bluff.country == country).count()
    logger.info(f"n_latest: {n_latest}")
    skip = random.randint(0, n_latest-1)
    latest: Bluff = await Bluff.find(Bluff.date >= sod).skip(skip).first_or_none()
    lines = latest.message.split("\n")
    return templates.TemplateResponse("bluff.html", {"request":request, "bluff_lines": lines})

@app.get("/team/{team}", response_class=HTMLResponse)
async def get_bluff(request: Request, team: str):
    sod = get_start_of_day()
    n_latest: Bluff = await Bluff.find(Bluff.date >= sod, Or(Bluff.team1 == team, Bluff.team2 == team)).count()
    while n_latest == 0:
        sod = sod - dt.timedelta(days=1)
        n_latest: Bluff = await Bluff.find(Bluff.date >= sod, Or(Bluff.team1 == team, Bluff.team2 == team)).count()
    logger.info(f"n_latest: {n_latest}")
    skip = random.randint(0, n_latest-1)
    latest: Bluff = await Bluff.find(Bluff.date >= sod).skip(skip).first_or_none()
    lines = latest.message.split("\n")
    return templates.TemplateResponse("bluff.html", {"request":request, "bluff_lines": lines})

@app.get("/cup/{cup}", response_class=HTMLResponse)
async def get_bluff(request: Request, cup: str):
    sod = get_start_of_day()
    n_latest: Bluff = await Bluff.find(Bluff.date >= sod, Bluff.cup == cup).count()
    while n_latest == 0:
        sod = sod - dt.timedelta(days=1)
        n_latest: Bluff = await Bluff.find(Bluff.date >= sod, Bluff.cup == cup).count()
    logger.info(f"n_latest: {n_latest}")
    skip = random.randint(0, n_latest-1)
    latest: Bluff = await Bluff.find(Bluff.date >= sod).skip(skip).first_or_none()
    lines = latest.message.split("\n")
    return templates.TemplateResponse("bluff.html", {"request":request, "bluff_lines": lines})


@app.post("/refresh/bluffs", dependencies=[Depends(check_access_token)])
async def post_bluff():
    logger.info("refreshing bluffs")
    await refresh_bluffs()
    return {"status": "ok"}


@app.post("/refresh/transfers",  dependencies=[Depends(check_access_token)])
async def post_transfer(request: Request):
    logger.info("refreshing transfers")
    await persist_transfers.get_and_persist_transfers()
    return {"status": "ok"}


@app.post("/refresh/fixtures",  dependencies=[Depends(check_access_token)])
async def post_fixture(request: Request):
    logger.info("refreshing fixtures")
    await persist_matches.get_and_persist_fixtures()
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, log_level="info")
