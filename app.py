from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.openai_parser import parse_user_prompt
from services.discogs_service import fetch_tracks_by_intent
from services.spotify_service import get_spotify_links

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

@app.post("/", response_class=HTMLResponse)
async def chat_handler(request: Request, prompt: str = Form(...)):
    try:
        # Step 1: Parse the prompt
        parsed_intent = parse_user_prompt(prompt)

        # Step 2: Query Discogs for tracks based on intent
        raw_tracks = fetch_tracks_by_intent(parsed_intent)

        # Step 3: Refine and get Spotify links
        refined_results = get_spotify_links(raw_tracks)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": refined_results,
            "prompt": prompt
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": None,
            "error": str(e),
            "prompt": prompt
        })