from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import numpy as np
import pandas as pd
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:

    def __init__(self):
        client_id = os.environ['SPOTIFY_CLIENT_ID']
        client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotipy = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def fetch_basic_artist_info(self, artist_uri):
        return self.spotipy.artist(artist_uri)

    def fetch_artist_albums(self, artist_uri):
        sp_albums = self.spotipy.artist_albums(artist_uri, album_type='album')
        album_names = []
        album_uris = []
        for i in range(len(sp_albums['items'])):
            album_names.append(sp_albums['items'][i]['name'])
            album_uris.append(sp_albums['items'][i]['uri'])
        return album_names, album_uris

    def fetch_album_songs(self, album_uri, album_name):
        spotify_album = {'album': [], 'track_number': [], 'id': [], 'name': [], 'uri': []}
        tracks = self.spotipy.album_tracks(album_uri)
        print(tracks)

        for n in range(len(tracks['items'])):  # for each song track
            spotify_album['album'].append(album_name)  # append album name tracked via album_count
            spotify_album['track_number'].append(tracks['items'][n]['track_number'])
            spotify_album['id'].append(tracks['items'][n]['id'])
            spotify_album['name'].append(tracks['items'][n]['name'])
            spotify_album['uri'].append(tracks['items'][n]['uri'])
        return spotify_album

    def fetch_audio_features(self, track_uri_list):
        pass

    def __chunk_spotify_track_uri_list(self, track_uri_list, limit=50):
        for i in range(0, len(track_uri_list), limit):
            yield track_uri_list[i:i + limit]

    def get_albums_by_artist_from_list(self, artist_names):
        artists_album_names = {}
        artists_album_uris = {}
        for artist in artist_names:
            album_names, album_uris = self.fetch_artist_albums(artist)
            if album_names is not None and album_uris is not None:
                artists_album_names[artist] = album_names
                artists_album_uris[artist] = album_uris
        return artists_album_names, artists_album_uris
