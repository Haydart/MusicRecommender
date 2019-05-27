def __chunk_spotify_track_uri_list(track_uri_list, limit=50):
    for i in range(0, len(track_uri_list), limit):
        yield track_uri_list[i:i + limit]
