import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .title-text {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #333333;
        margin-bottom: 10px;
        font-family: sans-serif;
    }

    div[data-testid="stTabs"] button {
        flex: 1;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 15px 0;
        border-radius: 0px;
        border-bottom: 2px solid #f0f2f6;
        color: #555;
    }

    /* Selected Tab */
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #FF4B4B;
        border-bottom: 4px solid #FF4B4B;
    }

    /* Hover */
    div[data-testid="stTabs"] button:hover {
        color: #FF4B4B;
    }

    .stTabs {
        margin-top: 0px;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_auth():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    if not client_id:
        st.error("Error authentication")
        return None

    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-top-read user-read-recently-played",
        cache_path=".spotify_cache",
        open_browser=False
    )

def get_spotify_user():
    auth_manager = get_auth()
    if auth_manager:
        return spotipy.Spotify(auth_manager=auth_manager)
    return None

def display_top_artists(sp, time_range):
    try:
        data = sp.current_user_top_artists(limit=10, time_range=time_range)
        st.write("")

        for i, item in enumerate(data['items']):
            c1, c2 = st.columns([1, 4])
            with c1:
                if item['images']:
                    st.image(item['images'][0]['url'], use_container_width=True)
            with c2:
                st.subheader(f"{i + 1}. {item['name']}")
                st.caption(", ".join([g.title() for g in item['genres'][:2]]))
            st.divider()
    except Exception as e:
        st.error("Error loading top artists")

def display_top_tracks(sp, time_range):
    try:
        data = sp.current_user_top_tracks(limit=10, time_range=time_range)
        st.write("")

        for i, item in enumerate(data['items']):
            c1, c2 = st.columns([1, 4])
            with c1:
                if item['album']['images']:
                    st.image(item['album']['images'][0]['url'], use_container_width=True)
            with c2:
                st.subheader(f"{i + 1}. {item['name']}")
                st.write(f"{item['artists'][0]['name']}")
            st.divider()
    except:
        st.error("Error loading top tracks")

def main():
    st.markdown('<div class="title-text">My Music Stats</div>', unsafe_allow_html=True)

    sp = get_spotify_user()
    if not sp:
        return
    tab_artists, tab_tracks, tab_recent = st.tabs(["Top Artists", "Top Tracks", "Recently Played"])

    # Top artists
    with tab_artists:
        subtab_4w, subtab_6m, subtab_1y = st.tabs(["4 Weeks", "6 Months", "1 Year"])

        with subtab_4w:
            display_top_artists(sp, "short_term")
        with subtab_6m:
            display_top_artists(sp, "medium_term")
        with subtab_1y:
            display_top_artists(sp, "long_term")

    # Top tracks
    with tab_tracks:
        subtab_t_4w, subtab_t_6m, subtab_t_1y = st.tabs(["4 Weeks", "6 Months", "1 Year"])

        with subtab_t_4w:
            display_top_tracks(sp, "short_term")
        with subtab_t_6m:
            display_top_tracks(sp, "medium_term")
        with subtab_t_1y:
            display_top_tracks(sp, "long_term")

    # Recently played
    with tab_recent:
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        try:
            data = sp.current_user_recently_played(limit=15)
            bucharest_tz = pytz.timezone('Europe/Bucharest')

            for item in data['items']:
                track = item['track']
                played_at = item['played_at'].replace('Z', '+00:00')
                dt = datetime.fromisoformat(played_at).astimezone(bucharest_tz)

                c1, c2, c3 = st.columns([1, 3, 1])
                with c1:
                    if track['album']['images']: st.image(track['album']['images'][0]['url'], use_container_width=True)
                with c2:
                    st.markdown(f"**{track['name']}**")
                    st.caption(track['artists'][0]['name'])
                with c3:
                    st.text(dt.strftime("%H:%M"))
                    st.caption(dt.strftime("%d %b"))
                st.divider()
        except:
            st.error("Error loading recently played tracks")

if __name__ == "__main__":
    main()