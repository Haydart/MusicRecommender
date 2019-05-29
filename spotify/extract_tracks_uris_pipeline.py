import pandas as pd
from spotify.spotify_client import SpotifyClient
import time
import numpy as np

albums_df = pd.read_csv("../output/spotify_artists_albums_uris_output.csv")
print(f'{len(albums_df)} albums before deduplication')
albums_df = albums_df.drop_duplicates(subset=['album_uri'])
print(f'{len(albums_df)} albums after deduplication')

album_count_limit = 20
client = SpotifyClient()
result = []
batch_index = 7999
iterations_count = int(len(albums_df.index) / album_count_limit)

albums_uris_nd = albums_df['album_uri'].values
albums_names_nd = albums_df['album name'].values
artists_uris_nd = albums_df['artist uri'].values
artists_names_nd = albums_df['name'].values

full_column_names = ['artist name', 'artist uri', 'album name', 'album_uri', 'track name', 'track uri']
partial_column_names = ['artist name', 'album name', 'track name', 'track uri']

for lower_index in range(0, len(albums_df.index), album_count_limit):
    batch_index = batch_index + 1

    artists_names_batch = artists_names_nd[lower_index:min(lower_index + album_count_limit, len(albums_df.index)), ]
    artists_uris_batch = artists_uris_nd[lower_index:min(lower_index + album_count_limit, len(albums_df.index)), ]
    albums_names_batch = albums_names_nd[lower_index:min(lower_index + album_count_limit, len(albums_df.index)), ]
    albums_uris_batch = albums_uris_nd[lower_index:min(lower_index + album_count_limit, len(albums_df.index)), ]

    albums_tracks = client.fetch_albums_tracks(albums_uris_batch)

    for album_index, album_tracks in enumerate(albums_tracks):
        for track in album_tracks:
            result.append(
                [artists_names_batch[album_index], artists_uris_batch[album_index], albums_names_batch[album_index],
                 albums_uris_batch[album_index], track[0], track[1]])

    if batch_index % 500 == 0:
        print(f'DONE {batch_index} OUT OF {iterations_count} ALBUM BATCHES\t{time.ctime(int(time.time()))}')
        result_nd = np.array(result)
        result_df = pd.DataFrame(result_nd, columns=full_column_names)
        result = []
        with open('../output/spotify_artists_albums_tracks_output_full.csv', 'a', encoding='utf-8', newline='') as file:
            result_df.to_csv(file, header=False, index=False, encoding='utf-8')
        with open('../output/spotify_artists_albums_tracks_output.csv', 'a', encoding='utf-8', newline='') as file:
            result_df[partial_column_names].to_csv(file, header=False, index=False, encoding='utf-8')
