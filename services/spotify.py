import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

AUTH_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"

def get_spotify_access_token():
    response = requests.post(
        AUTH_URL,
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )
    response.raise_for_status()
    return response.json()["access_token"]

def search_spotify_tracks(titles, artist_name):
    token = get_spotify_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    spotify_results = []
    seen = set()

    for item in titles:
        query = f"{item['title']} {artist_name}"
        params = {
            "q": query,
            "type": "track",
            "limit": 1
        }
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        data = response.json()

        tracks = data.get("tracks", {}).get("items", [])
        if not tracks:
            continue

        track = tracks[0]
        title = track["name"]
        url = track["external_urls"]["spotify"]
        if title in seen:
            continue

        seen.add(title)
        spotify_results.append({
            "title": title,
            "artist": artist_name,
            "spotify_url": url
        })

    return spotify_results
