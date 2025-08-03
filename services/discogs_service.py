import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCOGS_USER_TOKEN = os.getenv("DISCOGS_TOKEN")

BASE_URL = "https://api.discogs.com/database/search"

HEADERS = {
    "User-Agent": "VibeCheck/1.0"
}

def clean_title(title):
    # Remove non-English characters and known junk
    return title.encode('ascii', errors='ignore').decode().strip()

def fetch_tracks_by_intent(artist, intent_type, decade=None):
    role_map = {
        "songs_by": "artist",
        "songs_featuring": "artist",
        "songs_produced_by": "producer",
        "songs_written_by": "written-by"
    }

    role = role_map.get(intent_type, "artist")
    year_range = ""

    if decade:
        start = int(decade)
        year_range = f"&year={start}-{start + 9}"

    query_url = f"{BASE_URL}?{role}={artist}&type=release&per_page=30{year_range}&token={DISCOGS_USER_TOKEN}"
    response = requests.get(query_url, headers=HEADERS)
    data = response.json()

    results = []
    seen = set()

    for result in data.get("results", []):
        title = clean_title(result.get("title", ""))
        if title in seen or not title or "remix" in title.lower() or "karaoke" in title.lower():
            continue

        seen.add(title)
        results.append({
            "title": title,
            "year": result.get("year", ""),
            "id": result.get("id", ""),
            "resource_url": result.get("resource_url", "")
        })

    return results[:10]  # Limit to 10 clean tracks
