from spotipy import SpotifyException
import random


def _get_artist_id_from_link(link):
    """Get artist id from link"""
    artist_id = f"spotify:artist:{link[link.rfind('t/') + 2: link.find('?')]}"
    return artist_id


def _search_for_artist(sp, term):
    """Search for an artist"""
    artists = sp.search(q=term, limit=10, type='artist')
    # Maybe add query for which of the artists they want, for now we'll just pick the top one
    artist_uri = artists['artists']['items'][0]['uri']
    return artist_uri


def _playlist_from_artist(sp, artist_name):
    """Create a playlist of songs that are similar to the specified artist's songs"""
    # Find related artists
    try:
        artist_id = _search_for_artist(sp, artist_name)
    except SpotifyException:
        print('No artist found.')
        return

    try:
        related_artists = sp.artist_related_artists(artist_id=artist_id)
    except SpotifyException:
        print('Artist has no related artists.')
        return

    # Find top songs from related artists
    top_tracks_uris = []
    for artist in related_artists['artists']:
        top_tracks = sp.artist_top_tracks(artist_id=artist['uri'])
        for track in top_tracks['tracks']:
            top_tracks_uris.append(track['uri'])

    # Create a new playlist
    current_user = sp.current_user()
    user_id = current_user['id']

    artist = sp.artist(artist_id=artist_id)
    artist_name = artist['name']
    related_artists_playlist = sp.user_playlist_create(user=user_id, name=f'Similar to {artist_name}')
    playlist_id = related_artists_playlist['id']

    # Add 100 random top songs to the new playlist
    random.shuffle(top_tracks_uris)
    top_tracks_uris = top_tracks_uris[0:100] if len(top_tracks_uris) >= 100 else top_tracks_uris
    sp.playlist_add_items(playlist_id=playlist_id, items=top_tracks_uris)
    print('Playlist Created!')
