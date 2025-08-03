import requests

DISCOGS_API_BASE = "https://api.discogs.com"
DISCOGS_USER_AGENT = "VibeCheck/1.0"
DISCOGS_TOKEN = "YOUR_DISCOGS_TOKEN_HERE"

HEADERS = {
    "User-Agent": DISCOGS_USER_AGENT,
    "Authorization": f"Discogs token={DISCOGS_TOKEN}"
}

def search_90s_songs_by_artist(artist_name):
    search_url = f"{DISCOGS_API_BASE}/database/search"
    params = {
        "artist": artist_name,
        "type": "release",
        "format": "Vinyl, Single, EP, Album",
        "year": "1990-1999",
        "per_page": 50,
        "token": DISCOGS_TOKEN
    }

    response = requests.get(search_url, headers=HEADERS, params=params)
    results = response.json().get("results", [])

    unique_tracks = set()
    cleaned_results = []

    for r in results:
        title = r.get("title", "")
        if artist_name.lower() not in title.lower():
            continue

        # Avoid duplicates and foreign releases
        if any(x in title for x in ["=", "＝", "瑪麗亞", "マライア", "Mariah Carey ="]):
            continue

        if title not in unique_tracks:
            unique_tracks.add(title)
            cleaned_results.append({
                "title": title,
                "year": r.get("year"),
                "label": r.get("label", []),
                "format": r.get("format", []),
                "resource_url": r.get("resource_url")
            })

        if len(cleaned_results) >= 10:
            break

    return cleaned_results
