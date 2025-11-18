from flask import Flask, render_template, request, redirect, session, url_for
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from spotifyAnalysis import (
    recently_played_tracks, 
    top_tracks, top_artists, 
    genre_distribution, 
    get_usr_profile, 
    get_spotify_client
    )


app = Flask(__name__)
app.secret_key = os.urandom(24)
@app.route("/callback")
def callback():
    auth_manager = SpotifyOAuth(
        client_id = os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read user-read-recently-played user-read-private"
    )
    auth_manager.get_access_token(request.args.get("code"))
    return redirect("/")



@app.route("/")
def home():
    sp, access_token = get_spotify_client()

    user_profile = get_usr_profile(access_token)
    if not sp:
        auth_manager = SpotifyOAuth(
        client_id = os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read user-read-recently-played user-read-private"
        )
        return redirect(auth_manager.get_authorize_url())

    user_profile = get_usr_profile(access_token)
    display_name = user_profile.get('display_name', 'User')
    images = user_profile.get('images', [])
    profile_image_url = images[0]['url'] if images else url_for('static', filename='img/default-avatar.png')
    tracks = recently_played_tracks(sp)
    top = top_tracks(sp)
    artistTop = top_artists(sp)
    genre_data = genre_distribution(sp)
    total_tracks = len(tracks)

    all_genres = []
    for artist in artistTop:
        genres = artist.get('genres', [])
        if isinstance(genres, list):
            all_genres.extend(genres)
        elif isinstance(genres, str):
            all_genres.append(genres)

    genre_counts = Counter(all_genres)
    top_genre = genre_counts.most_common(1)[0][0] if genre_counts else "Unknown"

    hours = []
    for track in tracks:
        dt = datetime.strptime(track['played_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        hours.append(dt.hour)    
    hours_count = Counter(hours)
    peak_hour = hours_count.most_common(1)[0][0] if hours_count else 'Unknown'

    top_artist = artistTop[0] if artistTop else {}
    top_artist_url = top_artist.get('url', '')
    top_artist_name = top_artist.get('name', 'Unknown')
    top_artist_genre = ', '.join(top_artist.get('genres', [])) if top_artist.get('genres') else 'Unknown'




    return render_template("index.html",
                                display_name=display_name,
                                tracks=tracks,
                                top_tracks=top,
                                top_artists=artistTop,
                                genre_data=genre_data,
                                profile_image_url=profile_image_url,
                                total_tracks=total_tracks,
                                top_genre=top_genre,
                                peak_hour=peak_hour,
                                top_artist_url=top_artist_url,
                                top_artist_name=top_artist_name,
                                top_artist_genre=top_artist_genre,
                           )




if __name__ == '__main__':
    app.run(debug=True, port=8888)