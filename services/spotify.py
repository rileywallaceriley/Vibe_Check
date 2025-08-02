import requests
import os
import base64

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

def get_spotify_token():
    auth = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth.encode()).decode()
    res = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {b64_auth}"},
        data={"grant_type": "client_credentials"}
    )
    return res.json().get("access_token")

def get_spotify_links(track_list):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    links = []
    for track in track_list:
        res = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params={"q": track, "type": "track", "limit": 1}
        )
        items = res.json().get("tracks", {}).get("items", [])
        if items:
            track_info = items[0]
            links.append({
                "name": track_info["name"],
                "artist": track_info["artists"][0]["name"],
                "spotify_url": track_info["external_urls"]["spotify"]
            })
    return links
