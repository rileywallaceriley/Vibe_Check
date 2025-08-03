import requests
import os

DISCOGS_TOKEN = os.environ.get("DISCOGS_USER_TOKEN")

def get_discogs_tracks(intent):
    name = intent.get("name")
    role = intent.get("role")
    decade = intent.get("decade")

    params = {
        "token": DISCOGS_TOKEN,
        "per_page": 30,
        "type": "release"
    }

    if role == "primary_artist":
        params["artist"] = name
    else:
        params["credit"] = name

    if decade:
        if decade == "1990s":
            params["year"] = "1990"
        elif decade == "2000s":
            params["year"] = "2000"
        # You could expand this logic to handle ranges

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
        if "Compilation" in title or "Various" in title:
            continue
        seen.add(title)
        playlist.append(f"{title} ({year})")
        if len(playlist) >= 10:
            break

    return playlist
