from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.discogs import get_discogs_tracks
from services.spotify import get_spotify_links
from services.openai_parser import parse_user_prompt

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

session_store = {}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_handler(request: Request):
    data = await request.json()
    prompt = data.get("prompt")

    # Use OpenAI to understand the prompt
    parsed_intent = parse_user_prompt(prompt)

    if "error" in parsed_intent:
        return JSONResponse({"raw_playlist": [], "message": "Sorry, I couldn't understand that."})

    # Use intent info to generate playlist
    raw_tracks = get_discogs_tracks(parsed_intent)
    session_store["last_tracks"] = raw_tracks

    return JSONResponse({
        "raw_playlist": raw_tracks,
        "message": f"Here’s a list of songs {parsed_intent['role'].replace('_', ' ')} by {parsed_intent['name']}. Want Spotify links?"
    })

@app.post("/links")
async def link_handler(request: Request):
    track_list = session_store.get("last_tracks", [])
    links = get_spotify_links(track_list)
    return JSONResponse({"linked_playlist": links})
