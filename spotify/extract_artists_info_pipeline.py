import pandas as pd
from spotify.spotify_client import SpotifyClient
import time
import numpy as np

artists_df = pd.read_csv("../output/every_noise_artists_output.csv")
print(f'{len(artists_df)} artists before deduplication')

done_artists_df = artists_df.drop_duplicates(subset=['spotify_artist_id'], keep=False)
artists_df = artists_df.drop_duplicates(subset=['spotify_artist_id'])
artists_df = pd.concat([artists_df, done_artists_df])
artists_df = artists_df.reset_index(drop=True)
artists_df = artists_df.drop_duplicates(subset='spotify_artist_id', keep=False)
artists_df = artists_df.reset_index(drop=True)

print(f'{len(artists_df)} artists after deduplication')

client = SpotifyClient()
result = []
index = 0

for _, artist in artists_df[['name', 'spotify_artist_id']].iterrows():
    index = index + 1
    albums_names, albums_uris = client.fetch_artist_albums(artist['spotify_artist_id'])

    for album_name, album_uri in zip(albums_names, albums_uris):
        # print(artist['name'], artist['spotify_artist_id'], album_name, album_uri)
        result.append([artist['name'], artist['spotify_artist_id'], album_name, album_uri])

    if index % 100 == 0:
        print(f'DONE {index} ARTISTS\t{time.ctime(int(time.time()))}')
        result_nd = np.array(result)
        result_df = pd.DataFrame(result_nd, columns=['name', 'artist uri', 'album name', 'album_uri'])
        result = []
        with open('../output/spotify_artists_albums_uri.csv', 'a') as file:
            result_df.to_csv(file, header=False, index=False)
