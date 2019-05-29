import pandas as pd
from spotify.spotify_client import SpotifyClient
import time
import numpy as np

tracks_df = pd.read_csv("../output/spotify_artists_albums_tracks_output_full.csv")
print(f'{len(tracks_df)} tracks before deduplication')
tracks_df = tracks_df.drop_duplicates(subset=['album uri'])
print(f'{len(tracks_df)} tracks after deduplication')

artists_names_nd = tracks_df['artist name'].values
artists_uris_nd = tracks_df['artist uri'].values
albums_names_nd = tracks_df['album name'].values
albums_uris_nd = tracks_df['album uri'].values
tracks_names_nd = tracks_df['track name'].values
tracks_uris_nd = tracks_df['track uri'].values

track_count_limit = 50
client = SpotifyClient()
result = []
batch_index = 0
iterations_count = int(len(tracks_df.index) / track_count_limit)

added_column_names = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                      'liveness', 'valence', 'tempo', 'duration_ms']

for lower_index in range(0, len(tracks_df.index), track_count_limit):
    batch_index = batch_index + 1

    artists_names_batch = artists_names_nd[lower_index:min(lower_index + track_count_limit, len(tracks_df.index)), ]
    artists_uris_batch = artists_uris_nd[lower_index:min(lower_index + track_count_limit, len(tracks_df.index)), ]
    albums_names_batch = albums_names_nd[lower_index:min(lower_index + track_count_limit, len(tracks_df.index)), ]
    albums_uris_batch = albums_uris_nd[lower_index:min(lower_index + track_count_limit, len(tracks_df.index)), ]
    tracks_names_batch = tracks_names_nd[lower_index:min(lower_index + track_count_limit, len(tracks_df.index)), ]
    tracks_uris_batch = tracks_uris_nd[lower_index:min(lower_index + track_count_limit, len(tracks_df.index)), ]

    tracks_features = client.fetch_audio_features(tracks_uris_batch)

