import pandas as pd
from spotify.spotify_client import SpotifyClient
import time
import numpy as np

tracks_df = pd.read_csv("../output/spotify_artists_albums_tracks_output.csv")
print(f'{len(tracks_df)} tracks before deduplication')
tracks_df = tracks_df.drop_duplicates(subset=['album uri'])
print(f'{len(tracks_df)} tracks after deduplication')

albums_names_nd = tracks_df['album name'].values
albums_uris_nd = tracks_df['album uri'].values
tracks_names_nd = tracks_df['track name'].values
tracks_uris_nd = tracks_df['track uri'].values
tracks_df.drop("track uri", axis=1, inplace=True)

track_count_limit = 50
client = SpotifyClient()
result = []
batch_index = 0
iterations_count = int(len(tracks_df.index) / track_count_limit)

result_column_names = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                       'liveness', 'valence', 'tempo', 'duration_ms']
