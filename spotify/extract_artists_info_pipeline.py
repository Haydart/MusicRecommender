import pandas as pd
from spotify.spotify_client import SpotifyClient

artists_df = pd.read_csv("../output/artists_output.csv")
print(artists_df.head())
print(f'Overall artist-genre pairs: {len(artists_df.index)}')
print(f'Unique artists: {len(artists_df["spotify_artist_id"].unique())}')

client = SpotifyClient()

artist_id = artists_df.loc[artists_df['name'] == 'Disturbed'].iloc[0]['spotify_artist_id']
print(f'artist id: {artist_id}')
print(client.fetch_basic_artist_info(artist_id))
album_names, album_uris = client.fetch_artist_albums(artist_id, filter_albums=True)
print(album_names)
print(album_uris)
# print(client.fetch_album_songs(album_uris[2], album_names[2]))
print("fetching albums info")
print(client.fetch_albums_data(album_uris))

