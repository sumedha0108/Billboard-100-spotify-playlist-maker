import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

#date = input("Which year do you want to travel to? format - YYYY:MM:DD")

url = f"https://www.billboard.com/charts/hot-100/2016-08-12/"
resp = requests.get(url)
webpage = resp.text

soup = BeautifulSoup(webpage, "html.parser")


names = soup.select(selector="li li h3")
songs= []
for i in names:
    songs.append(i.getText().strip())


client_id = os.getenv('C_ID')
client_secret = os.getenv('C_SECRET')

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private playlist-modify-public",
        client_id = client_id,
        client_secret=client_secret,
        redirect_uri="http://example.com",
        username="Sumedha",
        cache_path="token.txt",
        show_dialog=True
    ))

user_id = sp.current_user()["id"]
#print(user_id)

song_uris = []

for song in songs:
    res = sp.search(q=f"track:{song} year:2016", type="track")
    try:
        uri = res["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#print(song_uris)

playlist = sp.user_playlist_create(user=user_id, name="Billboard Hot 100 2016-12-08")
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

