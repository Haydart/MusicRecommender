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

    def fetch_albums_data(self, album_uri_list, filter_albums=True, filter_tracks=True):
        if len(album_uri_list) > 20:
            raise ConnectionRefusedError('Cannot process more than 20 albums at once')
        response = self.spotipy.albums(album_uri_list)
        names_to_uris = [{album['name']: album['uri']} for album in response['albums']]


        tracks = [[{track['name'] : track['uri']} for track in album['tracks']['items']] for album in response['albums']]
        return names_to_uris, tracks

    def fetch_audio_features(self, track_uri_list):
        pass
