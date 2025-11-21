from dotenv import load_dotenv
import os
import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth


if __name__ == "__main__":
    load_dotenv()

    scope = "user-library-read playlist-modify-public"
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_URI"),
            scope=scope,
            username=os.getenv("SPOTIFY_USERNAME"),
        )
    )

    archive = "0vfGrDILx6BZpH4Mdk2Xxl"
    discover_weekly = "37i9dQZEVXcHxwNSmqEXRi"

    id_pattern = re.compile(r'href="/track/([a-zA-Z0-9]+)"')

    headers = {"Accept-Encoding": "identity"}
    page = requests.get(f"https://open.spotify.com/playlist/{discover_weekly}", headers)

    spotify.playlist_add_items(archive, id_pattern.findall(page.text))
