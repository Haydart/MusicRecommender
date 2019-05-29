import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
from utils.utils import list_duplicate_indices


class SpotifyClient:

    def __init__(self):
        client_id = os.environ['SPOTIFY_CLIENT_ID']
        client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotipy = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.unwanted_album_name_keywords = ['live', 'remix', 'remaster', 'remastered']
        self.feature_names = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                              'liveness', 'valence', 'tempo', 'duration_ms']
        self.empty_features = [None] * len(self.feature_names)

    def fetch_basic_artist_info(self, artist_uris):
        return self.spotipy.artists(artist_uris)

    def fetch_artist_albums(self, artist_uri):
        response = self.spotipy.artist_albums(artist_uri, album_type='album')
        albums_names = []
        albums_uris = []
        for i in range(len(response['items'])):
            albums_names.append(response['items'][i]['name'])
            albums_uris.append(response['items'][i]['uri'])

        albums_names, albums_uris = self.__filter_duplicated_albums(albums_names, albums_uris)
        albums_names, albums_uris = self.__filter_albums_with_keywords(albums_names, albums_uris)
        return self.__filter_subset_albums(albums_names, albums_uris)

    def __filter_duplicated_albums(self, albums_names, albums_uris):
        while any(tup[1] > 1 for tup in Counter(albums_names).most_common()):  # while duplicated album names exist
            duplicates_list = [list_duplicate_indices(albums_names, item) for item in albums_names]
            index_to_drop = next(duplicate[0] for duplicate in duplicates_list if len(duplicate) > 1)
            del albums_names[index_to_drop]
            del albums_uris[index_to_drop]
        return albums_names, albums_uris

    def __filter_albums_with_keywords(self, albums_names, albums_uris):
        album_names_to_drop = [checked_album_name for checked_album_name in albums_names for unwanted_keyword in
                               [unwanted_keyword for unwanted_keyword in self.unwanted_album_name_keywords] if
                               unwanted_keyword in checked_album_name.lower()]
        album_indices_to_drop = [albums_names.index(album_name) for album_name in album_names_to_drop]
        album_uris_to_drop = [albums_uris[index] for index in album_indices_to_drop]

        return self.__drop_albums(album_names_to_drop, album_uris_to_drop, albums_names, albums_uris)

    def __drop_albums(self, album_names_to_drop, album_uris_to_drop, albums_names, albums_uris):
        for album_name in album_names_to_drop:
            if album_name in albums_names:
                albums_names.remove(album_name)
        for album_uri in album_uris_to_drop:
            if album_uri in albums_uris:
                albums_uris.remove(album_uri)
        return albums_names, albums_uris

    def __filter_subset_albums(self, albums_names, albums_uris):
        album_names_to_drop = [checked_album_name for checked_album_name in albums_names for album_name in
                               [album_name for album_name in albums_names] if
                               checked_album_name in album_name and checked_album_name is not album_name]
        album_indices_to_drop = [albums_names.index(album_name) for album_name in album_names_to_drop]
        album_uris_to_drop = [albums_uris[index] for index in album_indices_to_drop]

        return self.__drop_albums(album_names_to_drop, album_uris_to_drop, albums_names, albums_uris)

    def fetch_albums_tracks(self, album_uri_list):
        response = self.spotipy.albums(album_uri_list)
        tracks = [[(track['name'], track['uri']) for track in album['tracks']['items']] for album in response['albums']]
        return tracks

    def fetch_audio_features(self, track_uri_list):
        response = self.spotipy.audio_features(track_uri_list)
        return ([track[feature_name] for feature_name in self.feature_names] if track else self.empty_features
                for track in response)


if __name__ == '__main__':
    client = SpotifyClient()
    print(client.fetch_artist_albums('spotify:artist:221Rd0FvVxMx7eCbWqjiKd'))
    print(client.fetch_audio_features(['spotify:track:1IlcTlRl6t59ZsY4spAZus', 'spotify:track:0O8hrovSEOyFnHDZiMCeml']))
