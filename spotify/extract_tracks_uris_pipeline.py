import pandas as pd
from spotify.spotify_client import SpotifyClient

albums_df = pd.read_csv("../output/spotify_artists_albums_uris_output.csv")
print(f'{len(albums_df)} albums before deduplication')
albums_df = albums_df.drop_duplicates(subset=['album_uri'])
print(f'{len(albums_df)} albums after deduplication')

client = SpotifyClient()
