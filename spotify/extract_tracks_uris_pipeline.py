import pandas as pd
from spotify.spotify_client import SpotifyClient
import time

albums_df = pd.read_csv("../output/spotify_artists_albums_uris_output.csv")
print(f'{len(albums_df)} albums before deduplication')
albums_df = albums_df.drop_duplicates(subset=['album_uri'])
print(f'{len(albums_df)} albums after deduplication')

album_count_limit = 20
client = SpotifyClient()
result = []
index = 0
iterations_count = int(len(albums_df.index)/album_count_limit)

albums_uris_nd = albums_df['album_uri'].values


for i in range(0, len(albums_df.index), album_count_limit):

    # print(tracks, '\n')

