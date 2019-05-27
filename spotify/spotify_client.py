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

    def fetch_artist(self, spotify_artist_id):
        return self.spotipy.artist(spotify_artist_id)


