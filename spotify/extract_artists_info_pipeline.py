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

print(artist_ids)
print(client.fetch_basic_artist_info(artist_ids))
print(client.fetch_artist_albums(artist_ids))