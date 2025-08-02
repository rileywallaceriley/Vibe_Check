import requests
import os

DISCOGS_TOKEN = os.environ.get("DISCOGS_USER_TOKEN")

def get_discogs_tracks(prompt):
    artist = prompt.replace("songs featuring", "").strip()
    url = "https://api.discogs.com/database/search"
    params = {"q": artist, "type": "release", "token": DISCOGS_TOKEN}
    res = requests.get(url, params=params)
    results = res.json().get("results", [])
    tracks = [f"{r.get('title')} ({r.get('year')})" for r in results]
    return tracks[:10]
