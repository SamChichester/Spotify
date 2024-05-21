import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from playlist_from_artist import _playlist_from_artist


class Spotify:
    def __init__(self, scope):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=scope,
                client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
                redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URI')
            )
        )

    def create_playlist_from_artist(self, artist):
        _playlist_from_artist(self.sp, artist)


if __name__ == '__main__':
    scope = "playlist-modify-public"
    bot = Spotify(scope)
    bot.create_playlist_from_artist('Soundgarden')  # Artist name goes here
