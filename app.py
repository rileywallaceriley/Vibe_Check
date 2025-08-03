from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.discogs import get_discogs_tracks
from services.spotify import get_spotify_links

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Store track list in memory (for demo)
session_store = {}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_handler(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    raw_tracks = get_discogs_tracks(prompt)

    # Save session (simplified)
    session_store["last_tracks"] = raw_tracks

    return JSONResponse({
        "raw_playlist": raw_tracks,
        "message": "Here’s your raw list. Want me to grab Spotify links too?"
    })

@app.post("/links")
async def link_handler(request: Request):
    track_list = session_store.get("last_tracks", [])
    links = get_spotify_links(track_list)
    return JSONResponse({"linked_playlist": links})