from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import start_beanie_session
from db.gpt import Bluff

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_beanie_session()
    

app.mount("/static", StaticFiles(directory="./src/app/static"), name="static")


templates = Jinja2Templates(directory="./src/app/templates")


@app.get("/", response_class=HTMLResponse)
async def get_bluff(request: Request):
    latest: Bluff = await Bluff.find().sort(-Bluff.date).limit(1).first_or_none()
    lines = latest.message.split("\n")
    return templates.TemplateResponse("bluff.html", {"request":request, "bluff_lines": lines})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, log_level="info")