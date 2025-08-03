from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from services.openai_parser import parse_user_prompt
from services.discogs_service import fetch_tracks_by_intent
from services.spotify_service import get_spotify_links
from jinja2 import Environment, FileSystemLoader
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")


@app.get("/", response_class=HTMLResponse)
async def form_get():
    return template.render(results=None)


@app.post("/", response_class=HTMLResponse)
async def chat_handler(request: Request):
    form_data = await request.form()
    prompt = form_data["prompt"]

    parsed_prompt = parse_user_prompt(prompt)
    raw_tracks = await fetch_tracks_by_intent(parsed_prompt, "songs")
    final_tracks = await get_spotify_links(raw_tracks)

    return template.render(results=final_tracks, prompt=prompt)