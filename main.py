import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = "user-top-read user-read-recently-played"

def authentication():
    if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        raise ValueError("Spofify API credentials not found")

    print("-- Starting authentication --")

    user = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotify_cache",
    ))

    print("-- Authentication complete --")
    return user


def get_and_display_data(sp_user):
    print("USER'S TOP 5 ARTISTS (Last Year)\n")

    try:
        top_artists_result = sp_user.current_user_top_artists(
            limit=5,
            time_range='long_term'
        )

        for i, artist in enumerate(top_artists_result['items']):
            print(f"[{i + 1}] {artist['name']} (Genres: {', '.join(artist['genres'][:2])})")

    except Exception as e:
        print(f"Error getting top artists: {e}")

    print("\nUSER'S TOP 5 SONGS (Last Year)\n")

    try:
        top_tracks_result = sp_user.current_user_top_tracks(
            limit=5,
            time_range='long_term'
        )

        for i, track in enumerate(top_tracks_result['items']):
            artist_names = ", ".join([artist['name'] for artist in track['artists']])
            print(f"[{i + 1}] {track['name']} by {artist_names}")

    except Exception as e:
        print(f"Error getting top tracks: {e}")

    print("\nUSER'S RECENTLY PLAYED SONGS\n")

    try:
        recently_played_results = sp_user.current_user_recently_played(limit=10)

        for i, item in enumerate(recently_played_results['items']):
            track = item['track']
            artist_names = ", ".join([artist['name'] for artist in track['artists']])

            # Formatting timestamp
            bucharest_time_zone = pytz.timezone('Europe/Bucharest')
            played_at_utc = item['played_at']
            dt_object = datetime.strptime(played_at_utc.split('.')[0] + 'Z', "%Y-%m-%dT%H:%M:%SZ")
            dt_object_utc = pytz.utc.localize(dt_object)
            dt_object_bucharest = dt_object_utc.astimezone(bucharest_time_zone)
            formatted_time = dt_object_bucharest.strftime("%H:%M")

            print(f"[{i + 1}] {track['name']} by {artist_names} (Played: {formatted_time})")

    except Exception as e:
        print(f"Error getting recently played tracks: {e}")

if __name__ == "__main__":
    try:
        user = authentication()
        get_and_display_data(user)
    except Exception as e:
        print(e)