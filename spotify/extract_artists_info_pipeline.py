import pandas as pd
from spotify.spotify_client import SpotifyClient

artists_df = pd.read_csv("../output/every_noise_artists_output.csv")
print(artists_df.head())
print(f'Overall artist-genre pairs: {len(artists_df.index)}')
print(f'Unique artists: {len(artists_df["spotify_artist_id"].unique())}')

client = SpotifyClient()

artist_ids = [artists_df.loc[artists_df['name'] == 'Disturbed'].iloc[0]['spotify_artist_id'],
              artists_df.loc[artists_df['name'] == 'Avenged Sevenfold'].iloc[0]['spotify_artist_id'],
              artists_df.loc[artists_df['name'] == 'Dream Theater'].iloc[0]['spotify_artist_id'],
              artists_df.loc[artists_df['name'] == 'Saor'].iloc[0]['spotify_artist_id'],
              artists_df.loc[artists_df['name'] == 'Mgła'].iloc[0]['spotify_artist_id']]

print(f'artist id: {artist_ids[0]}')
print(client.fetch_basic_artist_info(artist_ids))
albums_names, albums_uris = client.fetch_artist_albums(artist_ids[0], filter_duplicate_names=True)
albums_tracks = client.fetch_albums_tracks(albums_uris)
print(albums_names)
print(albums_uris)
print(albums_tracks)