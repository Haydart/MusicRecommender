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

    def fetch_basic_artist_info(self, artist_uris):
        return self.spotipy.artists(artist_uris)

    def fetch_artist_albums(self, artist_uri, filter_duplicate_names=True, filter_subset_albums=True):
        response = self.spotipy.artist_albums(artist_uri, album_type='album')
        album_names = []
        album_uris = []
        for i in range(len(response['items'])):
            album_names.append(response['items'][i]['name'])
            album_uris.append(response['items'][i]['uri'])

        if filter_duplicate_names:
            unique_album_names, unique_album_uris = self.__filter_duplicated_albums(album_names, album_uris)

            if filter_subset_albums:
                return self.__filter_subset_albums(unique_album_names, album_uris)
            else:
                return unique_album_names, unique_album_uris
        else:
            return album_names, album_uris

    def __filter_duplicated_albums(self, album_names, album_uris):
        while any(tup[1] > 1 for tup in Counter(album_names).most_common()):  # while duplicated album names exist
            duplicates_list = [list_duplicate_indices(album_names, item) for item in album_names]
            index_to_drop = next(duplicate[0] for duplicate in duplicates_list if len(duplicate) > 1)
            del album_names[index_to_drop]
            del album_uris[index_to_drop]
        return album_names, album_uris

    def __filter_subset_albums(self, albums_names, albums_uris):
        album_names_to_drop = [checked_album_name for checked_album_name in albums_names for album_name in
                               [album_name for album_name in albums_names] if
                               checked_album_name in album_name and checked_album_name is not album_name]

        album_indices_to_drop = [albums_names.index(album_name) for album_name in album_names_to_drop]
        album_uris_to_drop = [albums_uris[index] for index in album_indices_to_drop]

        for album_name in album_names_to_drop:
            albums_names.remove(album_name)

        for album_uri in album_uris_to_drop:
            albums_uris.remove(album_uri)

        return albums_names, albums_uris

    # def fetch_album_songs(self, album_uri, album_name):
    #     spotify_album = {'album': [], 'track_number': [], 'id': [], 'name': [], 'uri': []}
    #     tracks = self.spotipy.album_tracks(album_uri)
    #     print(tracks)
    #
    #     for n in range(len(tracks['items'])):  # for each song track
    #         spotify_album['album'].append(album_name)  # append album name tracked via album_count
    #         spotify_album['track_number'].append(tracks['items'][n]['track_number'])
    #         spotify_album['id'].append(tracks['items'][n]['id'])
    #         spotify_album['name'].append(tracks['items'][n]['name'])
    #         spotify_album['uri'].append(tracks['items'][n]['uri'])
    #     return spotify_album

    def fetch_albums_tracks(self, album_uri_list):
        if len(album_uri_list) > 20:
            raise ConnectionRefusedError('Cannot process more than 20 albums at once')
        response = self.spotipy.albums(album_uri_list)
        albums = [(album['name'], album['uri']) for album in response['albums']]
        tracks = [[(track['name'], track['uri']) for track in album['tracks']['items']] for album in response['albums']]
        return tracks

    def fetch_audio_features(self, track_uri_list):
        pass
