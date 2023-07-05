import logging
import os
import random

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import start_beanie_session
from db.gpt import Bluff
from football_api.actions import persist_fixtures, persist_transfers
from gpt.actions.refresh_bluffs import refresh_bluffs
from utils.dateutils import get_start_of_day

WORKING_DIR = os.environ.get('SRC_DIR','/workspace/src')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_beanie_session()
    

#app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory=f"{WORKING_DIR}/app/templates")


@app.get("/", response_class=HTMLResponse)
async def get_bluff(request: Request):
    sod = get_start_of_day()
    n_latest: Bluff = await Bluff.find(Bluff.date >= sod).count()
    logger.info(f"n_latest: {n_latest}")
    skip = random.randint(0, n_latest-1)
    latest: Bluff = await Bluff.find(Bluff.date >= sod).skip(skip).first_or_none()
    lines = latest.message.split("\n")
    return templates.TemplateResponse("bluff.html", {"request":request, "bluff_lines": lines})


@app.post("/refresh/bluffs")
async def post_bluff(request: Request):
    logger.info("refreshing bluffs")
    await refresh_bluffs()
    return {"status": "ok"}


@app.post("/refresh/transfers")
async def post_transfer(request: Request):
    logger.info("refreshing transfers")
    await persist_transfers.get_and_persist_transfers()
    return {"status": "ok"}


@app.post("/refresh/fixtures")
async def post_fixture(request: Request):
    logger.info("refreshing fixtures")
    await persist_fixtures.get_and_persist_fixtures()
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, log_level="info")
