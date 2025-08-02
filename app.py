from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.discogs import get_discogs_tracks
from services.spotify import get_spotify_links

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_handler(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    raw_tracks = get_discogs_tracks(prompt)
    return JSONResponse({
        "raw_playlist": raw_tracks,
        "message": "Here’s your raw list. Want me to grab Spotify or YouTube links too?"
    })

@app.post("/links")
async def link_handler(request: Request):
    data = await request.json()
    tracks = data.get("tracks", [])
    service = data.get("service", "spotify")
    if service == "spotify":
        links = get_spotify_links(tracks)
    else:
        links = []
    return JSONResponse({"linked_playlist": links})
