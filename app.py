from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.openai_parser import parse_user_prompt
from services.discogs_service import fetch_tracks_by_intent
from services.spotify_service import get_spotify_links

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def chat_handler(request: Request):
    form_data = await request.form()
    prompt = form_data["prompt"]

    parsed_prompt = parse_user_prompt(prompt)
    raw_tracks = fetch_tracks_by_intent(parsed_prompt, "songs")  # removed await
    final_tracks = get_spotify_links(raw_tracks)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "tracks": final_tracks,
        "prompt": prompt
    })