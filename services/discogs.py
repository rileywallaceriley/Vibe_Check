import requests
import os
from utils.prompt_parser import parse_prompt

DISCOGS_TOKEN = os.environ.get("DISCOGS_USER_TOKEN")

def get_discogs_tracks(prompt):
    parsed = parse_prompt(prompt)
    name, role = parsed["name"], parsed["role"]

    params = {
        "token": DISCOGS_TOKEN,
        "per_page": 30,
        "type": "release"
    }

    if role == "primary_artist":
        params["artist"] = name
    else:
        params["credit"] = name

    url = "https://api.discogs.com/database/search"
    res = requests.get(url, params=params)
    results = res.json().get("results", [])

    seen = set()
    playlist = []

    for r in results:
        title = r.get("title")
        year = r.get("year")
        if not title or title in seen:
            continue
        seen.add(title)
        playlist.append(f"{title} ({year})")
        if len(playlist) >= 10:
            break

    return playlist