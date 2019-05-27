import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
from .utils import list_duplicate_indices


class SpotifyClient:

    def __init__(self):
        client_id = os.environ['SPOTIFY_CLIENT_ID']
        client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotipy = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.unwanted_album_name_keywords = ['live', 'remix', 'remaster', 'remastered']

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
        print(albums_names)
        album_names_to_drop = [checked_album_name for checked_album_name in albums_names for unwanted_keyword in
                               [unwanted_keyword for unwanted_keyword in self.unwanted_album_name_keywords] if
                               unwanted_keyword in checked_album_name.lower()]
        album_indices_to_drop = [albums_names.index(album_name) for album_name in album_names_to_drop]
        album_uris_to_drop = [albums_uris[index] for index in album_indices_to_drop]

        return self.__drop_albums(album_names_to_drop, album_uris_to_drop, albums_names, albums_uris)

    def __drop_albums(self, album_names_to_drop, album_uris_to_drop, albums_names, albums_uris):
        for album_name in album_names_to_drop:
            albums_names.remove(album_name)
        for album_uri in album_uris_to_drop:
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
        if len(album_uri_list) > 20:
            raise ConnectionRefusedError('Cannot process more than 20 albums at once')
        response = self.spotipy.albums(album_uri_list)
        albums = [(album['name'], album['uri']) for album in response['albums']]
        tracks = [[(track['name'], track['uri']) for track in album['tracks']['items']] for album in response['albums']]
        return tracks

    def fetch_audio_features(self, track_uri_list):
        pass
