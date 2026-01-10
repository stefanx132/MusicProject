import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

def get_clean_env(var_name):
    val = os.getenv(var_name)
    if val:
        return val.strip().strip('"').strip("'")
    return None

CLIENT_ID = get_clean_env("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = get_clean_env("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = get_clean_env("SPOTIPY_REDIRECT_URI")
        return val.strip().strip('"').strip("'")
    return None

CLIENT_ID = get_clean_env("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = get_clean_env("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = get_clean_env("SPOTIPY_REDIRECT_URI")
CACHE_CONTENT = os.getenv("SPOTIPY_CACHE") 

SCOPE = "user-top-read user-read-recently-played"

def authentication():
    if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        raise ValueError("Spotify API credentials not found")

    print("-- Starting authentication --")

    cache_path = ".spotify_cache_file"

    if CACHE_CONTENT:
        clean_content = CACHE_CONTENT.strip()
        while clean_content.startswith(("'","\"")) or clean_content.endswith(("'","\"")):
            clean_content = clean_content.strip("'").strip('"')

        try:
            json_data = json.loads(clean_content)
            with open(cache_path, "w") as f:
                json.dump(json_data, f)
        except json.JSONDecodeError as e:
            print(f"EROARE CACHE: {e}")
            with open(cache_path, "w") as f:
                f.write(clean_content)

    try:
        user = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,# Acum este curat
            redirect_uri=REDIRECT_URI,
            with open(cache_path, "w") as f:
                f.write(clean_content)
    try:
        user = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=cache_path,
            open_browser=False
        ))
        user.me()
        print("-- Authentication complete --")
        return user
    except Exception as e:
        print(f"\nEROARE AUTENTIFICARE: {e}")
        print("Sfat: Verifică dacă Client ID și Secret din .env corespund cu contul care a generat cache-ul.")
        raise e

def get_and_display_data(sp_user):
    print("USER'S TOP 5 ARTISTS (Last Year)\n")
    try:
        top_artists_result = sp_user.current_user_top_artists(limit=5, time_range='long_term')
        for i, artist in enumerate(top_artists_result['items']):
            print(f"[{i + 1}] {artist['name']} (Genres: {', '.join(artist['genres'][:2])})")
    except Exception as e:
        print(f"Error getting top artists: {e}")

    print("\nUSER'S TOP 5 SONGS (Last Year)\n")
    try:
        top_tracks_result = sp_user.current_user_top_tracks(limit=5, time_range='long_term')
        for i, track in enumerate(top_tracks_result['items']):
            artist_names = ", ".join([artist['name'] for artist in track['artists']])
            print(f"[{i + 1}] {track['name']} by {artist_names}")
    except Exception as e:
        print(f"Error getting top tracks: {e}")

    print("\nUSER'S RECENTLY PLAYED SONGS\n")
    try:
        recently_played_results = sp_user.current_user_recently_played(limit=10)        for i, item in enumerate(recently_played_results['items']):
            track = item['track']
            artist_names = ", ".join([artist['name'] for artist in track['artists']])
            
            # Formatare timp
            bucharest_time_zone = pytz.timezone('Europe/Bucharest')
            played_at_utc_str = item['played_at'].replace('Z', '+00:00')
            try:
                dt_object = datetime.fromisoformat(played_at_utc_str)
            except ValueError:
                 dt_object = datetime.strptime(item['played_at'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                 dt_object = pytz.utc.localize(dt_object)
                 
            dt_object_bucharest = dt_object.astimezone(bucharest_time_zone)
            formatted_time = dt_object_bucharest.strftime("%H:%M")
            
            print(f"[{i + 1}] {track['name']} by {artist_names} (Played: {formatted_time})")
    except Exception as e:
        print(f"Error getting recently played tracks: {e}")

if __name__ == "__main__":
    try:
        user = authentication()
        get_and_display_data(user)
    except Exception as e:
        print("Script oprit din cauza erorilor.")
