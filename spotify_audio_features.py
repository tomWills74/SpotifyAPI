import os
import csv
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import RandomOverSampler
from dotenv import load_dotenv
load_dotenv()

from spotifyAnalysis import recently_played_tracks
from genres import manual_genre_map, genre_groups

RUN_DATA_COLLECTION = False

def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id = os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI"),
        scope = "user-read-private user-top-read user-read-recently-played"
    )
    sp = Spotify(auth_manager=auth_manager)
    return sp, sp.auth_manager.get_access_token(as_dict=False)

def get_artist_genre(sp, artist_name):
    results = sp.search(q=f'artist: {artist_name}', type='artist', limit=1)
    if results['artists']['items']:
        artist = results['artists']['items'][0]
        genres = artist['genres']
        return genres[0] if genres else 'Unknown'
    return "Unknown"

def generate_df(sp, limit=50, csv_path="listening_habits.csv"):
    data = []
    tracks = recently_played_tracks(sp, limit=limit)
    for track in tracks:
        name = track['name']
        artist = track['artists']
        played_at = track['played_at']
        genre = track['genre']

        timestamp = pd.to_datetime(played_at)
        hour = timestamp.hour
        day_of_week = timestamp.dayofweek
        is_weekend = 1 if day_of_week >=5 else 0

        data.append({
            'name': name,
            'artist': artist,
            'genre': genre,
            'played_at': played_at,
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'is_workday': 1 - is_weekend
        })

    df = pd.DataFrame(data)
    df['time_of_day'] = pd.cut(df['hour'],
                            bins=[-1, 6, 12, 18, 24],
                            labels=['Night', 'Morning', 'Afternoon', 'Evening'])
    # df = df.drop_duplicates(subset=['name', 'artist'])
    df['played_at'] = pd.to_datetime(df['played_at'])

    # load csv into function
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path, parse_dates=['played_at'])
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.drop_duplicates(subset=['name', 'artist', 'played_at'], inplace=True)
    else:
        combined_df = df

    # fill in missing genres
    genre_cache = {} 
    for idx, row in combined_df[combined_df['genre'] == 'Unknown'].iterrows():
        artist = row['artist']
        if artist not in genre_cache:
            genre_cache[artist] = get_artist_genre(sp, artist)
        combined_df.at[idx, 'genre'] = genre_cache[artist]
    
    combined_df.to_csv(csv_path, index=False)
    df = pd.read_csv("listening_habits.csv")
    # giving each entry a genre
    df['genre'] = df['artist'].map(manual_genre_map).fillna(df['genre'])

    # grouing the genres
    df['genre'] = df['genre'].map(genre_groups).fillna('other')
    df.to_csv("listening_habits_genre_mapped.csv", index=False)
    
    return combined_df

def train_model(csv_path="listening_habits_genre_mapped.csv"):
    df = pd.read_csv("listening_habits_genre_mapped.csv")
    df = df[df['genre'] != 'Unknown']
    features = ['hour', 'day_of_week', 'is_weekend', 'is_workday'] # , 'time_of_day', 'artist'
    X = df[features]
    y = df['genre']
    print(y.value_counts())

    le = LabelEncoder()
    y = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    ros = RandomOverSampler(random_state=42)
    X_train_res, y_train_res = ros.fit_resample(X_train, y_train)
    print("=" * 80)
    print(f"Training samples: {len(X_train_res)}")
    print(f"Testing samples: {len(X_test)}")
    print("=" * 80)
    models = {
        'logistic regression' : LogisticRegression(max_iter=1000),
        'random forest' : RandomForestClassifier(n_estimators=100, random_state=42),
        'decision tree classifier' : DecisionTreeClassifier(random_state=42),
        'knn' : KNeighborsClassifier(n_neighbors=5),
        'NB' : GaussianNB()
    }
    results = {}

    for name, model in models.items():
        model.fit(X_train_res, y_train_res)
        score = model.score(X_test, y_test)
        results[name] = score
        print(f"{name}: {score:.2%} accuracy")

    best_model = max(results, key=results.get)
    print("=" * 80)
    print(f"Best performing model is: {best_model}")
    return models[best_model], le

def predict_genre(model, le, hour, day_of_week, is_weekend, is_workday):
    input_data = pd.DataFrame({
        'hour': [hour],
        'day_of_week': [day_of_week],
        'is_weekend': [is_weekend],
        'is_workday': [is_workday]
    })
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    print("=" * 80)
    print(f"Predicted genre: {le.inverse_transform([prediction])[0]}")
    print("\nProbabilities:")
    for g, prob in zip(le.classes_, probabilities):
        print(f"  {g}: {prob:.1%}")
    return le.inverse_transform([prediction])[0]

if __name__ == "__main__":
    sp, _ = get_spotify_client()
    if RUN_DATA_COLLECTION:
        generate_df(sp)
        print("Collecting new listening data ...")
    else:
        print("=" * 80)
        print("Skipping data collection")
    print("=" * 80)

    model, le = train_model()
    import datetime
    now = datetime.datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    is_weekend = int(day_of_week >= 5)
    is_workday = int(day_of_week < 5)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    print(f"\nHey, its currently {hour}:00 on a {days[day_of_week]}. You should probably listen to some {predict_genre(model, le, hour=hour, day_of_week=day_of_week, is_weekend=is_weekend, is_workday=is_workday)} music")
    print("=" * 80)