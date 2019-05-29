import pandas as pd
from spotify.spotify_client import SpotifyClient
import time
import numpy as np

tracks_df = pd.read_csv("../output/spotify_artists_albums_tracks_output_full.csv")
print(f'{len(tracks_df)} tracks before deduplication')
tracks_df = tracks_df.drop_duplicates(subset=['track uri'])
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
start_batch_index = 18000
batch_index = start_batch_index
iterations_count = int(len(tracks_df.index) / track_count_limit)

added_column_names = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                      'liveness', 'valence', 'tempo', 'duration']
full_column_names = tracks_df.columns.tolist() + added_column_names
partial_column_names = [name for name in full_column_names if name not in ['artist uri', 'album uri', 'track uri']]

for lower_index in range(start_batch_index, len(tracks_df.index), track_count_limit):
    batch_index = batch_index + 1

    artists_names_batch = artists_names_nd[lower_index:lower_index + track_count_limit, ]
    artists_uris_batch = artists_uris_nd[lower_index:lower_index + track_count_limit, ]
    albums_names_batch = albums_names_nd[lower_index:lower_index + track_count_limit, ]
    albums_uris_batch = albums_uris_nd[lower_index:lower_index + track_count_limit, ]
    tracks_names_batch = tracks_names_nd[lower_index:lower_index + track_count_limit, ]
    tracks_uris_batch = tracks_uris_nd[lower_index:lower_index + track_count_limit, ]

    while True:
        try:
            tracks_features = client.fetch_audio_features(tracks_uris_batch)

            for track_index, track_features in enumerate(tracks_features):
                result.append(
                    [artists_names_batch[track_index], artists_uris_batch[track_index], albums_names_batch[track_index],
                     albums_uris_batch[track_index], tracks_names_batch[track_index],
                     tracks_uris_batch[track_index]] + track_features
                )

            if batch_index % 1000 == 0:
                print(f'DONE {batch_index} OUT OF {iterations_count} TRACK BATCHES\t{time.ctime(int(time.time()))}')
                result_nd = np.array(result)
                result_df = pd.DataFrame(result_nd, columns=full_column_names)
                result = []
                with open('../output/spotify_artists_albums_tracks_features_output_full.csv', 'a',
                          encoding='utf-8') as file:
                    result_df.to_csv(file, header=False, index=False, encoding='utf-8')
                with open('../output/spotify_artists_albums_tracks_features_output.csv', 'a', encoding='utf-8') as file:
                    result_df[partial_column_names].to_csv(file, header=False, index=False, encoding='utf-8')
        except:
            continue
        break
