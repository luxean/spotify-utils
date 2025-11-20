from dotenv import load_dotenv
import os
import spotipy
from itertools import batched
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
            username=os.getenv("USERNAME"),
        )
    )

    playlist = "1nAZGoZdXrLl2QCsnBELZ8"

    spotify.playlist_replace_items(playlist, [])

    offset = 0
    while True:
        # max 50 albums can be fetched at a time
        # https://developer.spotify.com/documentation/web-api/reference/get-users-saved-albums
        items = spotify.current_user_saved_albums(50, offset, "SK")["items"]
        if not items:
            break
        tracks = [
            track["uri"] for item in items for track in item["album"]["tracks"]["items"]
        ]
        # max 100 items can be added to a playlist at a time
        # https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
        for batch in batched(all_tracks, 100):
            spotify.playlist_add_items(playlist, batch)

        offset += len(items)
