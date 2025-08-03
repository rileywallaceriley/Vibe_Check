from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.openai_parser import parse_user_prompt
from services.discogs_service import fetch_tracks_by_intent
from services.spotify_service import get_spotify_links
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_handler(request: Request):
    form_data = await request.form()
    prompt = form_data["prompt"]

    try:
        parsed = json.loads(parse_user_prompt(prompt))
        artist = parsed.get("artist_name")
        intent_type = parsed.get("intent_type")
        decade = parsed.get("decade", None)

        raw_results = fetch_tracks_by_intent(artist, intent_type, decade)
        final_results = get_spotify_links(raw_results)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": final_results,
            "raw_prompt": prompt
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e),
            "raw_prompt": prompt
        })
