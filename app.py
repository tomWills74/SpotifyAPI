from flask import Flask, render_template, request, redirect, session, url_for
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from spotifyAnalysis import (
    recently_played_tracks, 
    top_tracks, top_artists, 
    genre_distribution, 
    get_usr_profile, 
    get_spotify_client
    )

load_dotenv()
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
    tracks = recently_played_tracks(sp)
    top = top_tracks(sp)
    artistTop = top_artists(sp)
    genre_data = genre_distribution(sp)

    return render_template("index.html",
                           display_name=display_name,
                           tracks=tracks,
                           top_tracks=top,
                           top_artists=artistTop,
                           genre_data=genre_data)




if __name__ == '__main__':
    app.run(debug=True, port=8888)