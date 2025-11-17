from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import requests
import os
from dotenv import load_dotenv
load_dotenv()
def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id = os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read user-read-recently-played user-read-private"
    )

    sp = Spotify(auth_manager=auth_manager)
    return sp, sp.auth_manager.get_access_token(as_dict=False)


def recently_played_tracks(sp, limit=10):
    recent = sp.current_user_recently_played(limit=limit)
    tracks = []
    for item in recent['items']:
        track = item['track']
        played_at = item['played_at']
        url = track['album']['images'][2]['url']if track['album']['images'] else None
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        genre = artist_info['genres'][0] if artist_info['genres'] else 'Unknown'
        tracks.append({
            'name': track['name'],
            'artists': ', '.join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'played_at': played_at,
            'genre': genre,
            'url': url
        })
    return tracks

def top_tracks(sp, time_range='long_term', limit=10):
    top = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    tracks = []
    for item in top['items']:
        url = item['album']['images'][2]['url'] if item['album']['images'] else None
        tracks.append({
            'id': item['id'],
            'name': item['name'],
            'artists': ', '.join([artist['name'] for artist in item['artists']]),
            'album': item['album']['name'],
            'popularity': item['popularity'],
            'url': url,
        })
    return tracks

def top_artists(sp, time_range='short_term', limit=10):
    top = sp.current_user_top_artists(time_range=time_range, limit=limit)
    artists = []
    for item in top['items']:
        url = item['images'][2]['url'] if item['images'] else None
        artists.append({
            'name': item['name'],
            'genres': ', '.join(item['genres']),
            'popularity': item['popularity'],
            'followers': item['followers']['total'],
            'url': url
        })
    return artists

def genre_distribution(sp):
    top = sp.current_user_top_artists(limit=50)
    genre_counter = Counter()
    for item in top['items']:
        for genre in item['genres']:
            genre_counter[genre] += 1
    genre_data = [{'genre': genre, 'count': count} for genre, count in genre_counter.items()]
    return genre_data

def get_usr_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("filed to parse JSON response")
            return None
    else:
        print(f"spotify api error: {response.status_code} - {response.text}")
        return None